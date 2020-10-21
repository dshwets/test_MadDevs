from django.shortcuts import render


def make_api_path(url):
    url_parts = url.split('/')
    if url_parts[2] == 'github.com':
        api_url = 'https://api.github.com/repos/'+ url_parts[3]+'/'+ url_parts[4] + '/commits'
        return api_url
    elif url_parts[2] == 'gitlab.com':
        api_url = 'https://gitlab.com/api/v4/projects/'+ url_parts[3]+'%2F'+ url_parts[4] \
                  + '/repository/commits/'
        return api_url

