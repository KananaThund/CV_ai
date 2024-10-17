import requests


def get_html(url: str):
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/58.0.3029.110 Safari/537.36"
        },
    )


# print(response.text)
# with open("vacancy.html", "w") as f:
#     f.write(response.text)

from bs4 import BeautifulSoup


def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Извлечение заголовка вакансии
    title = soup.find("h1", {"data-qa": "vacancy-title"})
    title = title.text.strip() if title else "Не указано"

    # Извлечение зарплаты
    salary = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"})
    salary = salary.text.strip() if salary else "Не указано"

    # Извлечение опыта работы
    experience = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience.text.strip() if experience else "Не указано"

    # Извлечение типа занятости и режима работы
    employment_mode = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode.text.strip() if employment_mode else "Не указано"

    # Извлечение компании
    company = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company.text.strip() if company else "Не указано"

    # Извлечение местоположения
    location = soup.find("p", {"data-qa": "vacancy-view-location"})
    location = location.text.strip() if location else "Не указано"

    # Извлечение описания вакансии
    description = soup.find("div", {"data-qa": "vacancy-description"})
    description = description.text.strip() if description else "Не указано"

    # Извлечение ключевых навыков
    skills = [
        skill.text.strip()
        for skill in soup.find_all(
            "div", {"class": "magritte-tag__label___YHV-o_3-0-3"}
        )
    ]

    # Формирование строки в формате Markdown
    markdown = f"""
# {title}

**Компания:** {company}
**Зарплата:** {salary}
**Опыт работы:** {experience}
**Тип занятости и режим работы:** {employment_mode}
**Местоположение:** {location}

## Описание вакансии
{description}

## Ключевые навыки
- {'\n- '.join(skills) if skills else 'Не указаны'}
"""

    return markdown.strip()


# from bs4 import BeautifulSoup

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение основных данных кандидата
    name_tag = soup.find('h2', {'data-qa': 'bloko-header-1'})
    name = name_tag.text.strip() if name_tag else "Не указано"

    gender_age_tag = soup.find('p')
    gender_age = gender_age_tag.text.strip() if gender_age_tag else "Не указано"

    location_tag = soup.find('span', {'data-qa': 'resume-personal-address'})
    location = location_tag.text.strip() if location_tag else "Не указано"

    job_title_tag = soup.find('span', {'data-qa': 'resume-block-title-position'})
    job_title = job_title_tag.text.strip() if job_title_tag else "Не указано"

    job_status_tag = soup.find('span', {'data-qa': 'job-search-status'})
    job_status = job_status_tag.text.strip() if job_status_tag else "Не указано"

    # Извлечение опыта работы
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experiences = []
    if experience_section:
        experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
        for item in experience_items:
            period_tag = item.find('div', class_='bloko-column_s-2')
            duration_tag = item.find('div', class_='bloko-text')
            period = period_tag.text.strip() if period_tag else "Не указано"
            duration = duration_tag.text.strip() if duration_tag else ""
            period = period.replace(duration, f" ({duration})") if duration else period

            company_tag = item.find('div', class_='bloko-text_strong')
            company = company_tag.text.strip() if company_tag else "Не указано"

            position_tag = item.find('div', {'data-qa': 'resume-block-experience-position'})
            position = position_tag.text.strip() if position_tag else "Не указано"

            description_tag = item.find('div', {'data-qa': 'resume-block-experience-description'})
            description = description_tag.text.strip() if description_tag else "Не указано"

            experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")
    else:
        experiences.append("Опыт работы не указан")

    # Извлечение ключевых навыков
    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = []
    if skills_section:
        skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})]
    else:
        skills.append("Ключевые навыки не указаны")

    # Формирование строки в формате Markdown
    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    for exp in experiences:
        markdown += exp + "\n"
    markdown += "## Ключевые навыки\n\n"
    markdown += ', '.join(skills) + "\n"

    return markdown



def get_candidate_info(url: str):
    response = get_html(url)
    return extract_candidate_data(response.text)


def get_job_description(url: str):
    response = get_html(url)
    return extract_vacancy_data(response.text)
