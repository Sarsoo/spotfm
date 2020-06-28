from fmframework.net.network import Network as FmNet, LastFMNetworkException
from spotframework.net.network import Network as SpotNet

from spotframework.model.uri import Uri
from spotframework.engine.playlistengine import TrackSource, SourceParameter
from spotframework.engine.processor.abstract import AbstractProcessor

from spotfm.charts.chart import get_chart_of_spotify_tracks

from typing import List
import logging

logger = logging.getLogger(__name__)


class ChartSource(TrackSource):
    class Params(SourceParameter):
        def __init__(self,
                     chart_range: FmNet.Range,
                     limit: int = 50,
                     processors: List[AbstractProcessor] = None):
            super().__init__(processors=processors, source_type=ChartSource)
            self.chart_range = chart_range
            self.limit = limit

    def __init__(self, spotnet: SpotNet, fmnet: SpotNet):
        super().__init__(net=spotnet)
        self.fmnet = fmnet

    def load(self):
        super().load()

    def process(self, params: Params, uris: List[Uri] = None):
        # TODO add processor support?

        try:
            return get_chart_of_spotify_tracks(spotnet=self.net,
                                               fmnet=self.fmnet,
                                               period=params.chart_range,
                                               limit=params.limit)
        except LastFMNetworkException as e:
            logger.error(f'error occured during chart retrieval - {e}')
