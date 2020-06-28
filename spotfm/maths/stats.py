from cmd import Cmd
import logging
import json

from spotframework.net.network import Network as Spotnet
from spotframework.engine.playlistengine import PlaylistEngine
from spotframework.model.uri import Uri
from fmframework.net.network import Network as Fmnet, LastFMNetworkException
from spotfm.maths.counter import Counter

logger = logging.getLogger(__name__)


class Stats(Cmd):
    intro = 'Stats... ? for help'
    prompt = '(stats)> '

    def __init__(self, spotnet: Spotnet, fmnet: Fmnet):
        Cmd.__init__(self)
        self.spotnet = spotnet
        self.fmnet = fmnet
        self.counter = Counter(spotnet=spotnet, fmnet=fmnet)

    def do_count(self, arg):
        """count spotify uri on last.fm"""

        in_string = arg

        if in_string is None or len(in_string) < 2:
            in_string = input('uri group/uri>')

        try:
            user_total = self.fmnet.get_user_scrobble_count()
        except LastFMNetworkException as e:
            logger.error(f'error occured during scrobble count retrieval - {e}')
            user_total = 0

        total = 0
        try:
            uri = Uri(in_string)
            total = self.counter.count(uri)
        except ValueError:
            with open('config/uri_groups.json', 'r') as file_obj:
                groups = json.load(file_obj)

                group = next((i for i in groups if i['name'] == in_string), None)
                if group is None:
                    print('group not found')
                    return

                counts = dict()
                for member in group['members']:
                    try:
                        uri_obj = Uri(member['uri'])
                        iter_count = self.counter.count(uri_obj)

                        counts.update({member['name']: iter_count})
                        total += iter_count
                    except ValueError:
                        print(f'malformed uri {uri_obj}')

                [print(f'{name} -> {count:,} scrobbles ({round((count*100)/total)}%)') for name, count in counts.items()]

        print(f'{in_string} -> {total:,} scrobbles ({round((total*100)/user_total, 2)}%)')

    def do_sort(self, arg):

        in_str = arg

        if in_str is None or len(arg) == 0:
            in_str = input('playlist>')

        if in_str is None or in_str == '':
            return

        engine = PlaylistEngine(self.spotnet)
        engine.reorder_playlist_by_added_date(in_str)
