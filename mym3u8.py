import re

import m3u8
from m3u8 import protocol
from m3u8.parser import save_segment_custom_value


def parse_attributes(line, lineno, data, state):
    if line.startswith(protocol.extinf):
        title = ''
        chunks = line.replace(protocol.extinf + ':', '').split(',', 1)
        if len(chunks) == 2:
            duration_and_props, title = chunks
        elif len(chunks) == 1:
            duration_and_props = chunks[0]

        additional_props = {}
        chunks = duration_and_props.strip().split(' ', 1)
        if len(chunks) == 2:
            duration, raw_props = chunks
            matched_props = re.finditer(r'([\w\-]+)="([^"]*)"', raw_props)
            for match in matched_props:
                additional_props[match.group(1)] = match.group(2)
        else:
            duration = duration_and_props

        if 'segment' not in state:
            state['segment'] = {}
        state['segment']['duration'] = float(duration)
        state['segment']['title'] = title

        # Helper function for saving custom values
        save_segment_custom_value(state, 'extinf_props', additional_props)

        # Tell 'main parser' that we expect an URL on next lines
        state['expect_segment'] = True

        # Tell 'main parser' that it can go to next line, we've parsed current fully.
        return True


class MyM3u8:
    def __init__(self, filename: str):
        self._playlist = m3u8.load(filename, custom_tags_parser=parse_attributes)

    def get_groups(self) -> iter:
        return list(set([segment.custom_parser_values['extinf_props']['group-title'] for segment in
                         self._playlist.segments if
                         'group-title' in segment.custom_parser_values['extinf_props'].keys()]))

    def extract_groups_from_list(self, groups: list) -> list:
        return [self.extract_group_from_list(group) for group in groups]

    def extract_group_from_list(self, group: str) -> str:
        playlist = [str(segment) for segment in self._playlist.segments if
                    'group-title' in segment.custom_parser_values['extinf_props'].keys() and group ==
                    segment.custom_parser_values['extinf_props']['group-title']]

        return '\n'.join(playlist)
