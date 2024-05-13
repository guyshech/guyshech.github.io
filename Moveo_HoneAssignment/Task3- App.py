import streamlit as st
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import google.generativeai as genai

# Make sure to insert your API key to run the app
genai.configure(api_key='YOUR_API_KEY')

# Function to get one-word topic from Gemini AI
def get_gemini_title_for_group(claims):
    model = genai.GenerativeModel('gemini-pro')
    claims_to_ai = 'Please give me a one word title that best describes the following claims' + '\n'.join(claims)
    response = model.generate_content(claims_to_ai)
    return response.text.strip()

# Function to run LDA clustering
def run_lda(claims, num_topics):
    # Vectorize claims text using CountVectorizer
    vectorizer = CountVectorizer()
    claims_counts = vectorizer.fit_transform(claims)

    # Apply LDA clustering
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(claims_counts)

    # Assign each claim to its corresponding topic
    topics = lda.transform(claims_counts).argmax(axis=1)

    # Group claims by topic
    grouped_claims = [[] for _ in range(num_topics)]
    for idx, topic in enumerate(topics):
        grouped_claims[topic].append(claims[idx])

    # Determine one-word topics for each group of claims
    group_topics = []
    for group_claims in grouped_claims:
        topic = get_gemini_title_for_group(group_claims)
        group_topics.append({'title': topic, 'number_of_claims': len(group_claims)})
    return group_topics

# Streamlit app
def main():
    st.title("Claim Clustering App")

    # List of all the claims from task 1
    claims = [
        "CLAIMS1. A wireless telephone apparatus comprising: a handset; an onioff-hook switch; a wireless communications module for establishing first and second cellular telephone calls via a base station; and means for generating an explicit call transfer command for sending to the base station in response to activation of the on-hook switch when the first and second wireless calls are established through the apparatus.",
        "2. The apparatus of claim 1, ftirther comprising a body having a cradle for the handset, wherein the onloff hook switch operates in response to placing the handset in the cradle.",
        "3. The apparatus of claim 1, 2 or 3, ftirther comprising: call receiving means for receiving a first call from a calling party; call initiating means for entering a call initiation mode, in response to activation of a first predetermined button, for initiating a second call; and transfer means for putting the first call on hold, initiating the second call, and toggling, in response to activation of the first predetermined button, between the first and second calls.",
        "4. The apparatus of claim 3, wherein the first predetermined button is a redial button.",
        "5. The apparatus of claim 3 or 4, wherein the transfer means toggles between the first and second calls by putting either the first or the second call on hold.",
        "6. The apparatus of any one of claims 3 to 5, further comprising means for enabling a phonebook lookup operation when in the call initiation mode.",
        "7. The apparatus of any one of claims 3 to 6, wherein the call initiation mode and a dialling mode are entered using the first predetermined button.",
        "8. The apparatus of any one of the preceding claims, further comprising display means for displaying first and second icons adjacent information relating to the first and second calls respectively, the first and second icons being adapted to switch when toggling between calls.",
        "9. The apparatus of claim 8, further comprising selection means for selecting information displayed on the display means.",
        "10. The apparatus of claim 8 or 9, wherein the transfer means is adapted to initiate a call to a second party whose information is displayed on the display means.",
        "11. The apparatus of any one of claims 3 to 10, further comprising a second predetermined button which ends an active call and reverts to a call on hold.",
        "12. The apparatus of claim 11, wherein the second predetermined button is a clear button.",
        "13. A method of effecting a call transfer comprising: establishing first and second cellular telephone calls at a wireless telephone apparatus, and generating an explicit call transfer command for sending to a base station in response to activation of an on-hook switch.",
        "14. A communication apparatus as substantially herein before described with reference to the accompanying drawings in Figures 1 to 7.",
        "15. A Method for a Media Gateway in connection to a backbone, comprising the steps of: measuring a packet loss or a jitter associated with said backbone, receiving a call when the measured packet loss exceeds a predefined packet loss threshold or when the measured jitter exceeds a predefined jitter threshold for said backbone; detecting an indication associated with the call, wherein the indication is based on a time period associated with the predefined packet loss threshold or the predefined jitter threshold, and wherein the indication indicates that the measured packet loss exceeding the predefined packet loss threshold or the measured jitter exceeding the predefined jitter threshold is acceptable for the call for said time period; based at least partially on the measured packet loss or the measured jitter and said indication associated with the call, deciding whether said call is admitted to be routed via said backbone; and adjusting the Quality of Service (QoS) level for said call when deciding said call is admitted via said backbone.",
        "16. The method according toclaim 1, wherein said indication is received from an external source such as a Mobile Switching Centre Server.",
        "17. The method according toclaim 1, wherein said indication is received in a Gateway Control Protocol (GCP) message.",
        "18. The method according toclaim 3, wherein said indication is a priority value within the GCP message.",
        "19. The method according toclaim 3, wherein said GCP message is a context request.",
        "20. The method according toclaim 1, wherein said indication is received from an internal source.",
        "21. The method according toclaim 1, further comprising routing said call through a second backbone further connected to said media gateway.",
        "22. The method according toclaim 6, wherein said internal source is a calendar.",
        "23. A Method for a Mobile Switching Centre Server in connection to a backbone, comprising the steps of: receiving a call set-up request associated with said backbone; detecting that the call set-up should be performed by a Media Gateway even when the measured packet loss is above a predefined packet loss threshold or when the measured jitter is above a predefined jitter threshold for said backbone; and providing an indication associated with the call to said Media Gateway, wherein the indication is based on a time period associated with the predefined packet loss threshold or the predefined jitter threshold, and wherein the indication indicates that the packet loss measurement above the predefined packet loss threshold or that the jitter measurement above the predefined jitter threshold is acceptable for said time period, and further indicating to admit the call via said backbone with a lower Quality of service accordingly, wherein said indication is received in a Gateway Control Protocol (GCP) message.",
        "24. The method according toclaim 9, wherein said step of detecting comprises: measuring a call gradient by analyzing call set-up events overtime, and detecting that the call set-up should be performed even when the measured packet loss is above a predefined packet loss threshold and/or when the measured jitter is above a predefined jitter threshold, when said gradient is above a predefined value.",
        "25. The method according toclaim 9, wherein said step of detecting further comprises: receiving an indication that a measured packet loss above the predefined packet loss threshold or a measured jitter above the predefined jitter threshold for an originator of said call is acceptable.",
        "26. The method according toclaim 9, wherein said step of detecting further comprises: receiving an indication that a measured packet loss above the predefined packet loss threshold or a measured jitter above the predefined jitter threshold for the destination of said call is acceptable.",
        "27. A Media Gateway comprising: means for connecting to a backbone; said means for connecting are configured to receive a call; processing means configured to measure a packet loss or a jitter for said backbone; said processing means are further configured to detect an indication associated with the call, wherein the indication is based on a time period associated with the predefined packet loss threshold or the predefined jitter threshold, and wherein the indication indicates that the measured packet loss above a predefined packet loss threshold or the measured jitter above a predefined jitter threshold is acceptable for said time period; said processing means are further configured to decide based at least partially on the measured packet loss or the measured jitter and said detected indication whether said call is admitted to be routed via said backbone even if the measured packet loss exceeds the predefined packet loss threshold or if the measured jitter exceeds the predefined jitter threshold; and said processing means are further configured to adjust the Quality of Service (QoS) level for said call when deciding said call is admitted to be routed via said backbone, wherein said indication is received in a Gateway Control Protocol (GCP) message.",
        "28. The Media Gateway according toclaim 13, wherein said means for connecting to said backbone are further configured to receive said indication from an external source such as a Mobile Switching Centre Server.",
        "29. The Media Gateway according toclaim 13, further comprising an internal source for providing said indication.",
        "30. The Media Gateway according toclaim 14, wherein said means for deciding are further configured to route said call through a second backbone further connected to said media gateway.",
        "31. A Mobile Switching Centre Server comprising: means for connecting to a backbone; said means for connecting are further configured to receive a call set-up request associated with said backbone; means for processing configured to detect that a call set-up should be performed by a Media Gateway even when a measured packet loss is above a predefined packet loss threshold or when a measured jitter is above a predefined jitter threshold for said backbone; and means for providing an indication associated with the call to the Media Gateway, wherein the indication is based on a time period associated with the predefined packet loss threshold or the predefined jitter threshold, and wherein the indication indicates that the measured packet loss above the predefined packet loss threshold or the measured jitter above the predefined jitter threshold is acceptable for said time period, and further indicating to admit the call via said backbone with a lower Quality of service accordingly.",
        "32. The Mobile Switching Centre Server according toclaim 17wherein: said means for processing are further configured to measure a call gradient by analyzing call set-up events over time; and said means for processing are further configured to detect that the call set-up should be performed even if the measured packet loss is above a predefined packet loss threshold or if the measured jitter is above a predefined jitter threshold if said gradient is above a predefined value.",
        "33. The Mobile Switching Centre Server according toclaim 17wherein said means for processing are further configured to receive an indication associated with the call indicating that a packet loss above the predefined packet loss threshold or a jitter above the predefined jitter threshold for an originator of said call is acceptable.",
        "34. The Mobile Switching Centre Server according toclaim 17wherein said means for processing are further configured to receive an indication associated with the call indicating that a measured packet loss above the predefined packet loss threshold or a measured jitter above the predefined jitter threshold for a destination of said call is acceptable.",
        "35. A system, comprising:a processor; anda memory that stores executable instructions that, when executed by the processor, facilitate performance of operations, comprising:obtaining a pressure-in to signal-out transfer function representing a distortion of an output signal of a microphone corresponding to an input stimulus of a defined sound pressure level (SPL) that has been applied to the microphone;creating an ideal sine wave stimulus based on an amplitude of a time domain waveform representing the output signal and a fundamental frequency of the time domain waveform;generating, based on a defined relationship between the ideal sine wave stimulus and the time domain waveform, an equation representing the pressure-in to signal-out transfer function representing the distortion of the output signal; andinverting the equation to obtain an inverse transfer function for facilitating an application, by the microphone, of the inverse transfer function to the output signal to obtain a linearized output representing the input stimulus.",
        "36. The system ofclaim 1, wherein the output signal is an output voltage, and wherein the obtaining comprises:measuring the output voltage.",
        "37. The system ofclaim 1, wherein the obtaining comprises:deriving, during a simulation of a defined model of the microphone comprising production based parameters of the microphone, the output signal.",
        "38. The system ofclaim 1, wherein the obtaining comprises:importing output data of the time domain waveform representing the output signal; andbased on the output data, obtaining properties of the time domain waveform comprising the amplitude of the time domain waveform and the fundamental frequency of the time domain waveform.",
        "39. The system ofclaim 1, wherein the defined relationship represents a voltage difference between the ideal sine wave stimulus and the time domain waveform with respect to a defined alignment of respective phases of the ideal sine wave stimulus and the time domain waveform.",
        "40. The system ofclaim 1, wherein the microphone comprises a micro-electro-mechanical system (MEMS) microphone.",
        "41. The system ofclaim 6, wherein the MEMS microphone comprises:a diaphragm that converts the SPL into an electrical signal;a single backplate capacitively coupled to a side of the diaphragm; andan electronic amplifier that buffers the electrical signal to generate the output signal.",
        "42. The system ofclaim 6, wherein the MEMS microphone comprises:a diaphragm that converts the SPL into an electrical signal;dual backplates capacitively coupled to respective sides of the diaphragm; andan electronic amplifier that buffers the electrical signal to generate the output signal.",
        "43. The system ofclaim 1, wherein the distortion comprises odd-order harmonic distortion and even-order harmonic distortion.",
        "44. The system ofclaim 9, wherein the distortion is not frequency dependent, and wherein the distortion is not time dependent.",
        "45. A micro-electro-mechanical system (MEMS) microphone, comprising:a processor; anda memory that stores executable instructions that, when executed by the processor, facilitate performance of operations, comprising:creating an ideal sine wave stimulus representing an output signal of the MEMS microphone with respect to an input stimulus of a defined sound pressure level (SPL) that has been applied to the MEMS microphone, wherein the ideal sine wave stimulus is based on an amplitude of a time domain waveform representing the output signal and a fundamental frequency of the time domain waveform;deriving, based on a defined relationship between the ideal sine wave stimulus and the time domain waveform, an equation of a transfer function representing a distortion of the output signal; andapplying, based on the equation, a linearization filter to the output signal to obtain a linearized output representing the input stimulus.",
        "46. The MEMS microphone ofclaim 11, wherein the output signal is an output voltage, and wherein the deriving the equation comprises:obtaining output data of the time domain waveform representing the output voltage; andbased on the output data, deriving properties of the time domain waveform comprising the amplitude of the time domain waveform and the fundamental frequency of the time domain waveform.",
        "47. The MEMS microphone ofclaim 11, further comprising:a diaphragm that converts the SPL into an electrical signal;a single backplate capacitively coupled to a side of the diaphragm; andan electronic amplifier that buffers the electrical signal to generate the output signal.",
        "48. The MEMS microphone ofclaim 11, further comprising:a diaphragm that converts the SPL into an electrical signal;dual backplates capacitively coupled to respective sides of the diaphragm; andan electronic amplifier that buffers the electrical signal to generate the output signal.",
        "49. The MEMS microphone ofclaim 11, wherein the defined relationship represents a voltage difference between the ideal sine wave stimulus and the time domain waveform with respect to a defined alignment of respective phases of the ideal sine wave stimulus and the time domain waveform.",
        "50. A method, comprising:generating, by a system comprising a processor, a sine wave stimulus representing an output signal of a microphone with respect to an input stimulus that has been applied to the microphone, wherein the sine wave stimulus is based on an amplitude of a time domain waveform representing the output signal and a fundamental frequency of the time domain waveform;selecting, by the system based on a defined relationship between the sine wave stimulus and the time domain waveform, an equation of a transfer function representing a distortion of the output signal; andfacilitating, by the system, an application, by the microphone, of an inversion of the equation to the output signal to obtain a linearized output representing the input stimulus.",
        "51. The method ofclaim 16, wherein the generating the sine wave stimulus comprises:obtaining data representing the output signal of the microphone; andgenerating the sine wave stimulus having the amplitude of the time domain waveform and the fundamental frequency of the time domain waveform.",
        "52. The method ofclaim 16, wherein the output signal is a voltage output, and wherein the selecting comprises:measuring, by the system, the voltage output.",
        "53. The method ofclaim 16, wherein the output signal is a voltage output, and wherein the selecting comprises:deriving, during a simulation of a defined model of the microphone based on defined production parameters corresponding to the microphone, the voltage output.",
        "54. The method ofclaim 16, wherein the selecting comprises:selecting the equation based on a voltage difference between the sine wave stimulus and the time domain waveform with respect to a defined alignment of respective phases of the sine wave stimulus and the time domain waveform.",
    ]

    # Slider for selecting number of groups
    num_groups = st.slider("Select number of groups:", min_value=1, max_value=len(claims), value=3)

    # Button to run clustering
    if st.button("Run Clustering"):
        # Run KMeans clustering
        groups = run_lda(claims, num_groups)

        # Display response
        st.json({'groups': groups})

if __name__ == "__main__":
    main()
