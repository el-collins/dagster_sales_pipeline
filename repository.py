from dagster import job, op
import requests

@op
def fetch_github_stars():
    response = requests.get('https://api.github.com/repos/dagster-io/dagster')
    print(response.json())
    return response.json()['stargazers_count']

@op
def display_stars(star_count):
    print(f'Dagster has {star_count} stars on GitHub.')

@job
def github_stats_job():
    display_stars(fetch_github_stars())
