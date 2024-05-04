select *
from PortfolioProject..CovidDeaths
order by 3,4

select *
from PortfolioProject..CovidVaccinations
order by 3,4

 --Select Data that we are going to be using

Select location, date, total_cases, new_cases, total_deaths, population
from PortfolioProject..CovidDeaths
order by 1,2

-- UPDATE All blank cells with NULL

update PortfolioProject..CovidVaccinations
set
    continent=nullif(continent, ''),
	location=nullif(location, ''),
	date=nullif(date, ''),
	population=nullif(population, ''),
	new_cases=nullif(new_cases, ''),
	new_cases_smoothed=nullif(new_cases_smoothed, ''),
	total_deaths=nullif(total_deaths, ''),
	new_deaths=nullif(new_deaths, ''),
	new_deaths_smoothed=nullif(new_deaths_smoothed, ''),
	total_cases=nullif(total_cases, ''),
	total_cases_per_million=nullif(total_cases_per_million, ''),
	new_cases_per_million=nullif(new_cases_per_million, ''),
	new_cases_smoothed_per_million=nullif(new_cases_smoothed_per_million, ''),
	total_deaths_per_million=nullif(total_deaths_per_million, ''),
	new_deaths_per_million=nullif(new_deaths_per_million, ''),
	new_deaths_smoothed_per_million=nullif(new_deaths_smoothed_per_million, ''),
	reproduction_rate=nullif(reproduction_rate, ''),
	icu_patients=nullif(icu_patients, ''),
	icu_patients_per_million=nullif(icu_patients_per_million, ''),
	hosp_patients=nullif(hosp_patients, ''),
	hosp_patients_per_million=nullif(hosp_patients_per_million, ''),
	weekly_icu_admissions=nullif(weekly_icu_admissions, ''),
	weekly_icu_admissions_per_million=nullif(weekly_icu_admissions_per_million, ''),
	weekly_hosp_admissions=nullif(weekly_hosp_admissions, ''),
	weekly_hosp_admissions_per_million=nullif(weekly_hosp_admissions_per_million, '')

-- UPDATE All blank cells with NULL

	update PortfolioProject..CovidVaccinations
	set
	total_tests=nullif(total_tests, ''),
new_tests=nullif(new_tests, ''),
total_tests_per_thousand=nullif(total_tests_per_thousand, ''),
new_tests_per_thousand=nullif(new_tests_per_thousand, ''),
new_tests_smoothed=nullif(new_tests_smoothed, ''),
new_tests_smoothed_per_thousand=nullif(new_tests_smoothed_per_thousand, ''),
positive_rate=nullif(positive_rate, ''),
tests_per_case=nullif(tests_per_case, ''),
tests_units=nullif(tests_units, ''),
total_vaccinations=nullif(total_vaccinations, ''),
people_vaccinated=nullif(people_vaccinated, ''),
people_fully_vaccinated=nullif(people_fully_vaccinated, ''),
total_boosters=nullif(total_boosters, ''),
new_vaccinations=nullif(new_vaccinations, ''),
new_vaccinations_smoothed=nullif(new_vaccinations_smoothed, ''),
total_vaccinations_per_hundred=nullif(total_vaccinations_per_hundred, ''),
people_vaccinated_per_hundred=nullif(people_vaccinated_per_hundred, ''),
people_fully_vaccinated_per_hundred=nullif(people_fully_vaccinated_per_hundred, ''),
total_boosters_per_hundred=nullif(total_boosters_per_hundred, ''),
new_vaccinations_smoothed_per_million=nullif(new_vaccinations_smoothed_per_million, ''),
new_people_vaccinated_smoothed=nullif(new_people_vaccinated_smoothed, ''),
new_people_vaccinated_smoothed_per_hundred=nullif(new_people_vaccinated_smoothed_per_hundred, ''),
stringency_index=nullif(stringency_index, ''),
population_density=nullif(population_density, ''),
median_age=nullif(median_age, ''),
aged_65_older=nullif(aged_65_older, ''),
aged_70_older=nullif(aged_70_older, ''),
gdp_per_capita=nullif(gdp_per_capita, ''),
extreme_poverty=nullif(extreme_poverty, ''),
cardiovasc_death_rate=nullif(cardiovasc_death_rate, ''),
diabetes_prevalence=nullif(diabetes_prevalence, ''),
female_smokers=nullif(female_smokers, ''),
male_smokers=nullif(male_smokers, ''),
handwashing_facilities=nullif(handwashing_facilities, ''),
hospital_beds_per_thousand=nullif(hospital_beds_per_thousand, ''),
life_expectancy=nullif(life_expectancy, ''),
human_development_index=nullif(human_development_index, ''),
excess_mortality_cumulative_absolute=nullif(excess_mortality_cumulative_absolute, ''),
excess_mortality_cumulative=nullif(excess_mortality_cumulative, ''),
excess_mortality=nullif(excess_mortality, ''),
excess_mortality_cumulative_per_million=nullif(excess_mortality_cumulative_per_million, '')

-- Looking at Toatal Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid in yout country 
Select location, date, total_cases, total_deaths, (cast(total_deaths as float)/cast(total_cases as float))*100 as DeathPercentage
From PortfolioProject..CovidDeaths
Where location like 'israel' and date like '%2021'
order by  1, 2


-- Looking at the Total Cases vs Population
-- Shows what precentage of population got covid

Select location, date, Population , total_cases, (cast(total_cases as float)/cast(Population as float))*100 as CovidPercentage
From PortfolioProject..CovidDeaths
-- Where location like 'israel' and date like '%2021'
order by  1, 2


-- Looking at Countries with Highest Infection Rate compared at Population
 --max((cast(total_cases as float)/cast(Population as float)))*100 as PercentPopulationInfected

SELECT 
    location, 
    Population, 
    MAX(total_cases) AS HighestInfectionCount, 
    (MAX(total_cases) / CAST(Population AS float)) * 100 AS PercentPopulationInfected
FROM PortfolioProject..CovidDeaths 
GROUP BY location, Population
ORDER BY PercentPopulationInfected DESC;

-- Showing Countries with Highest Death Count per Population

SELECT 
    location, MAX(cast(total_deaths as int)) AS TotaltDeathsCount 
FROM PortfolioProject..CovidDeaths 
Where continent is not null
GROUP BY location
ORDER BY TotaltDeathsCount DESC;

-- BREAKING THINGS DOWN BY CONTINENT

-- Showing contintents with the highest death count per population

Select continent, MAX(cast(Total_deaths as int)) as TotalDeathCount
From PortfolioProject..CovidDeaths
Where continent is not null 
Group by continent
order by TotalDeathCount desc


-- GLOBAL NUMBERS

Select SUM(cast(new_cases as int)) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as float))/SUM(cast(New_Cases as float))*100 as DeathPercentage
From PortfolioProject..CovidDeaths
where continent is not null 
--Group By date
order by 1,2



-- Total Population vs Vaccinations
-- Shows Percentage of Population that has recieved at least one Covid Vaccine

Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
order by 2,3


-- Using CTE to perform Calculation on Partition By in previous query

With PopvsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
--order by 2,3
)
Select *, (RollingPeopleVaccinated/Population)*100
From PopvsVac



-- Using Temp Table to perform Calculation on Partition By in previous query

DROP Table if exists #PercentPopulationVaccinated
Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date varchar(50),
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
--where dea.continent is not null 
--order by 2,3

Select *, (RollingPeopleVaccinated/Population)*100
From #PercentPopulationVaccinated




-- Creating View to store data for later visualizations

Create View PercentPopulationVaccinated as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
