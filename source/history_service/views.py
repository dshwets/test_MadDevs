from pip._vendor import requests

from history_service.models import CommitsHistory, Links

PER_PAGE = '100'

class CommitSaver:
    def __init__(self, LinkObject):
        self.object = LinkObject
        self.url = LinkObject.link
        self.url_parts = self.url.split('/')
        self.source = None
        # self.response = None
        # self.api_url = ''

    def _define_resource(self):
        if len(self.url_parts) < 5:
            raise ValueError('Url - не корректный')
        elif self.url_parts[2] == 'github.com':
            self.source = 'github'
        elif self.url_parts[2] == 'gitlab.com':
            self.source = 'gitlab'
        else:
            raise ValueError('Url - не корректный')

    def _make_api_path(self):
        self._define_resource()  # отладка.
        if self.source == 'github':
            api_url = 'https://api.github.com/repos/' + self.url_parts[3] + '/' + self.url_parts[
                4] + '/commits?per_page=' + PER_PAGE
            return api_url
        elif self.source == 'gitlab':
            api_url = 'https://gitlab.com/api/v4/projects/' + self.url_parts[3] + '%2F' + self.url_parts[4] \
                      + '/repository/commits?per_page=' + PER_PAGE
            return api_url
        else:
            raise ValueError('Url - не корректный')

    def _make_request(self):
        self._define_resource()
        response_list = []
        response = requests.get(self._make_api_path())
        if response.headers['status'].split(' ')[0] != '200':
            raise ValueError(f'Somthing went wrong \n {response.headers["status"]}')
        response_list.append(response.json())
        while True:
            if 'link' in response.headers or 'Link' in response.headers:
                if 'rel="next"' in response.headers['link'] or 'rel="next"' in response.headers['Link']:
                    if self.source == 'github':
                        links_list = response.headers['link'].split(',')
                    else:
                        links_list = response.headers['Link'].split(',')
                    for link in links_list:
                        if 'rel="next"' in link:
                            next_page = link
                            next_page = next_page.replace('rel="next"', '').strip().replace('<', '').replace('>',
                                                                                                             '').replace(
                                ';', '')
                            response = requests.get(next_page)
                            response_list.append(response.json())
                else:
                    break
            else:
                break
        return response_list

    def _save_or_update_db(self, commits_list):
        CommitsHistory.objects.bulk_create(commits_list)

    def _get_id_name(self):
        if self.source == 'github':
            return 'sha'
        else:
            return 'id'

    def save_commits_to_model(self):
        response_list = self._make_request()
        commit_histories = []
        current_commits = CommitsHistory.objects.all()
        id_name = self._get_id_name()
        for response in response_list:
            for commit in response:
                try:
                    current_commits.get(commit_id=commit[id_name])

                except TypeError:
                    raise TypeError('')
                except CommitsHistory.DoesNotExist:
                    commit_in_history = CommitsHistory(link=self.object, commit_id=commit[id_name], commit_json=commit)
                    commit_histories.append(commit_in_history)
        self._save_or_update_db(commit_histories)


class BulkCommitSaver:
    def __init__(self):
        self.repositories = Links.objects.all()

    def save_or_create_commits(self):
        print(self.repositories)
        for repository in self.repositories:
            print(repository)
            CommitSaver(repository).save_commits_to_model()
