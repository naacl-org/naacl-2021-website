import argparse
import itertools
import logging
import sys

from pathlib import Path

_THIS_DIR = Path(__file__).absolute().parent
AGENDA_SUBMODULE_DIR = _THIS_DIR.parent.joinpath('agenda', 'code')
print(AGENDA_SUBMODULE_DIR)
sys.path.append(str(AGENDA_SUBMODULE_DIR))

from orderfile import Agenda, SessionGroup, Session, Item
from metadata import ScheduleMetadata


class WebAgenda(Agenda):
    """
    Class encapsulating the agenda for the website.
    Inherits from `orderfile.Agenda` and adds a
    `to_html()` method to convert the parsed agenda
    into HTML for the website.
    """

    # define the starting static HTML that we need
    # before the actual schedule HTML
    _starting_html = ['<link rel="stylesheet" href="/assets/css/alertify.css" id="alertifyCSS">',
                      '<table id="hidden-program-table">',
                      '<thead>',
                      '<tr><th>time</th><th>location</th><th>info</th></tr>'
                      '</thead>',
                      '<tbody></tbody>',
                      '</table>',
                      '<div id="introParagraph">',
                      '<p>On this page, you can choose the sessions (and individual papers/posters) of your choice <em>and</em> generate a PDF of your customized schedule! This page should work on modern browsers on all operating systems. On mobile devices, Safari on iOS and Chrome on Android are the only browsers known to work. For the best experience, use a non-mobile device with a resolution of at least 1920x1080. For help, simply type "?"" while on the page or click on the "Help" button.</p>',
                      '</div>',
                      '<p class="text-center">',
                      '<a href="#" id="help-button" class="btn btn--small btn--twitter">Help</a>',
                      '</p>',
                      '<p class="text-center">',
                      '<a href="#" id="toggle-all-button" class="btn btn--small btn--twitter">Expand All Sessions ↓</a>',
                      '</p>',
                      '<div class="schedule">']

    # define the static HTML that goes at the end
    # of the actual schedule HTML
    _closing_html = ['<div id="generatePDFForm">',
                     '<div id="formContainer">',
                     '<input type="checkbox" id="includePlenaryCheckBox" value="second_checkbox"/>&nbsp;&nbsp;<span id="checkBoxLabel">Include plenary sessions in schedule</span>',
                     '<br/>',
                     '<a href="#" id="generatePDFButton" class="btn btn--twitter btn--large">Download PDF</a>'
                     '</div>',
                     '</div>',
                     '</div>']

    # define counters for session groups and breaks
    session_group_counter = itertools.count(start=1)
    break_session_counter = itertools.count(start=1)

    def __init__(self):
        super(WebAgenda, self).__init__()

    def to_html(self,
                metadata,
                paper_icons=False,
                video_icons=False):
        """
        Convert agenda to HTML format compatible
        with the NAACL 2019 GitHub pages theme.

        Parameters
        ----------
        metadata : ScheduleMetadata
            An instance of `ScheduleMetadata`
            containing the title, authors,
            abstracts, and anthology URLs for
            each item, if applicable.
        paper_icons : bool, optional
            Whether to generate the icons for
            each of the presentation items linked
            to the PDF on the anthology.
            Defaults to `False`.
        video_icons : bool, optional
            Whether to generate the icons for
            each of the oral presentation items
            linked to the video of the talk.
            Defaults to `False`.

        Returns
        -------
        agenda_html : str
            A string containing the schedule HTML.
        """

        # initialize the agenda HTML with the pre-schedule HTML
        agenda_html = WebAgenda._starting_html

        # iterate over the days in the agenda that should
        # already be in chronological order
        for day_index, day in enumerate(self.days):

            # generate HTML representing the day
            agenda_html.append('<div class="day" id="day-{}">{}</div>'.format(day_index + 1, str(day)))

            # now iterate over each day's contents
            for content in day.contents:

                # if it's a `SessionGroup`, cast it to the
                # `WebSessionGroup` class so that we can then
                # call its `to_html()` method; we do this by
                # monkeypatching the `__class__` attribute which
                # is fine since we are just adding new behavior
                # (methods), not new attributes.
                if isinstance(content, SessionGroup):
                    content.__class__ = WebSessionGroup
                    session_group_index = next(WebAgenda.session_group_counter)
                    session_group_html = content.to_html(day, metadata, session_group_index, paper_icons=paper_icons, video_icons=video_icons)
                    agenda_html.extend(session_group_html)

                # if it's a `Session`, then cast it to `WebSession`
                # and call its `to_html()` method and save that to
                # the agenda HTML.
                elif isinstance(content, Session):
                    content.__class__ = WebSession
                    index = next(WebAgenda.break_session_counter) if content.type == 'break' else None
                    session_html = content.to_html(day, metadata, index=index, paper_icons=paper_icons, video_icons=video_icons)
                    agenda_html.extend(session_html)

        # update with the post-schedule HTML
        agenda_html.extend(WebAgenda._closing_html)

        # convert the list to a string and return
        agenda_html = '\n'.join(agenda_html)
        return agenda_html


class WebSessionGroup(SessionGroup):
    """
    Class encapsulating a session group for the website.
    Inherits from `orderfile.SessionGroup` and adds a
    `to_html()` method to convert the parsed group
    into HTML for the website.
    """

    # initialize some counters we need
    parallel_paper_track_counter = itertools.cycle([1, 2, 3, 4, 5])
    poster_session_counter = itertools.count(start=1)

    def __init__(self):
        super(WebSessionGroup, self).__init__()

    def to_html(self,
                day,
                metadata,
                index,
                paper_icons=False,
                video_icons=False):
        """
        Convert session group to HTML format compatible
        with the NAACL 2019 GitHub pages theme.

        Parameters
        ----------
        day : orderfile.Day
            The `Day` instance on which the session
            group is scheduled.
        metadata : ScheduleMetadata
            An instance of `ScheduleMetadata`
            containing the title, authors,
            abstracts, and anthology URLs for
            each item, if applicable.
        index : int
            An index to be used in the HTML tags
            for the box representing this session group.
        paper_icons : bool, optional
            Whether to generate the icons for
            each of the presentation items linked
            to the PDF on the anthology.
            Defaults to `False`.
        video_icons : bool, optional
            Whether to generate the icons for
            each of the oral presentation items
            linked to the video of the talk.
            Defaults to `False`.

        Returns
        -------
        session_group_html : str
            A string containing the session group HTML.
        """

        # initialize the HTML with a box and header that goes in the HTML
        generated_html = ['<div class="session-box" id="session-box-{}">'.format(index)]
        generated_html.append('<div class="session-header" id="session-header-{}">{}</div>'.format(index, self.title))

        # iterate over the sessions in the group which should
        # already be in chronological order
        for session in self.sessions:

            # cast `Session` to `WebSession` to enable
            # the call to `to_html()`.
            session.__class__ = WebSession

            # the sessions in session groups do not
            # have a start and end time defined in the
            # order file, so we need to inherit those
            # here since sessions _are_ displayed with
            # start and end times on the website
            session.start = self.start
            session.end = self.end

            # call the respective `to_html()` for the session
            # and save the HTML
            if session.type == 'paper':
                index = next(WebSessionGroup.parallel_paper_track_counter)
            elif session.type == 'poster':
                index = next(WebSessionGroup.poster_session_counter)
            session_html = session.to_html(day,
                                           metadata,
                                           index=index,
                                           paper_icons=paper_icons,
                                           video_icons=video_icons)
            generated_html.extend(session_html)

        # add any required closing tags for valid HTML and return
        generated_html.append('</div>')
        return generated_html


class WebSession(Session):
    """
    Class encapsulating a session for the website.
    Inherits from `orderfile.Session` and adds a
    `to_html()` method to convert the parsed session
    into HTML for the website.

    """
    def __init__(self):
        super(WebSession, self).__init__()

    def to_html(self,
                day,
                metadata,
                index=None,
                paper_icons=False,
                video_icons=False):
        """
        Convert session to HTML format compatible
        with the NAACL 2019 GitHub pages theme.

        Parameters
        ----------
        day : orderfile.Day
            The `Day` instance on which the session
            is scheduled.
        metadata : ScheduleMetadata
            An instance of `ScheduleMetadata`
            containing the title, authors,
            abstracts, and anthology URLs for
            each item, if applicable.
        index : int, optional
            An index to be used in some of the HTML tags.
        paper_icons : bool, optional
            Whether to generate the icons for
            each of the presentation items linked
            to the PDF on the anthology.
            Defaults to `False`.
        video_icons : bool, optional
            Whether to generate the icons for
            each of the oral presentation items
            linked to the video of the talk.
            Defaults to `False`.

        Returns
        -------
        session_html : str
            A string containing the session HTML.
        """
        # initialize the result variable
        generated_html = []

        # generate the appropriate HTML for each type of session
        if self.type == 'break':
            generated_html.append('<div class="session session-break session-plenary" id="session-break-{}"><span class="session-title">{}</span><br/><span class="session-time" title="{}">{} &ndash; {}</span></div>'.format(index, self.title, str(day), self.start, self.end))

        elif self.type == 'plenary':
            generated_html.append('<div class="session session-plenary"><span class="session-title">{}</span><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/> <span class="session-location btn btn--location">{}</span></div>'.format(self.title, str(day), self.start, self.end, self.location))

        elif self.type == 'tutorial':

            # for tutorials, the session does not have start
            # and end times defined in the order file but we
            # need them for the website; so just get them from
            # the first session item
            self.start = self.items[0].start
            self.end = self.items[0].end

            generated_html.append('<div class="session session-expandable session-tutorials"><div id="expander"></div><a href="#" class="session-title">{}</a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><div class="tutorial-session-details"><br/><table class="tutorial-table">'.format(self.title, str(day), self.start, self.end, self.location))

            # we know tutorial sessions have child items, so
            # cast those `Item` objects as `WebItem`s, call
            # their `to_html()` methods and save the results
            for item in self.items:
                item.__class__ = WebItem
                item_html = item.to_html(metadata)
                generated_html.extend(item_html)

            # add any required closing tags for valid HTML
            generated_html.extend(['</table>', '</div>', '</div>'])

        elif self.type == 'best_paper':

            # the best paper session does not have start
            # and end times defined in the order file but we
            # need them for the website; so just get them from
            # the first and the last item
            self.start = self.items[0].start
            self.end = self.items[-1].end

            generated_html.append('<div class="session session-expandable session-papers-best"><div id="expander"></div><a href="#" class="session-title">{}</a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-location btn btn--location">{}</span><br/><div class="paper-session-details"><br/><table class="paper-table">'.format(self.title, str(day), self.start, self.end, self.location))

            # we know the best paper session has child items, so
            # cast those `Item` objects as `WebItem`s, call
            # their `to_html()` methods and save the results
            for item in self.items:
                item.__class__ = WebItem
                item_html = item.to_html(metadata,
                                         paper_icons=paper_icons,
                                         video_icons=video_icons)
                generated_html.extend(item_html)
            # add any required closing tags for valid HTML
            generated_html.extend(['</table>', '</div>', '</div>'])

        elif self.type == 'poster':
            generated_html.append('<div class="session session-expandable session-posters" id="session-poster-{}"><div id="expander"></div><a href="#" class="session-title">{}: {} </a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-location btn btn--location">{}</span><div class="poster-session-details"><br/><table class="poster-table">'.format(index, self.id_, self.title, str(day), self.start, self.end, self.location))

            # we know poster sessions have child items, so
            # cast those `Item` objects as `WebItem`s, call
            # their `to_html()` methods and save the results
            for item in self.items:
                item.__class__ = WebItem
                item_html = item.to_html(metadata,
                                         paper_icons=paper_icons)
                generated_html.extend(item_html)

            # add any required closing tags for valid HTML and return
            generated_html.extend(['</table>', '</div>', '</div>'])

        elif self.type == 'paper':
            generated_html.append('<div class="session session-expandable session-papers{}" id="session-{}"><div id="expander"></div><a href="#" class="session-title">{}: {}</a><br/><span class="session-time" title="{}">{} &ndash; {}</span><br/><span class="session-location btn btn--location">{}</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-{}-selector"> Choose All</a><a href="#" class="session-deselector" id="session-{}-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: {}</td></tr>'.format(index, self.id_.lower(), self.id_, self.title, str(day), self.start, self.end, self.location, self.id_.lower(), self.id_.lower(), self.chair))

            # we know paper sessions have child items, so
            # cast those `Item` objects as `WebItem`s, call
            # their `to_html()` methods and save the results
            for item in self.items:
                item.__class__ = WebItem
                item_html = item.to_html(metadata,
                                         paper_icons=paper_icons,
                                         video_icons=video_icons)
                generated_html.extend(item_html)

            # add any required closing tags for valid HTML and return
            generated_html.extend(['</table>', '</div>', '</div>'])

        return generated_html


class WebItem(Item):
    """
    Class encapsulating a presentation item for
    the website. Inherits from `orderfile.Item` and
    adds a `to_html()` method to convert the item
    into HTML for the website.

    """
    def __init__(self):
        super(WebItem, self).__init__()

    def to_html(self,
                metadata,
                paper_icons=False,
                video_icons=False):
        """
        Convert item to HTML format compatible
        with the NAACL 2019 GitHub pages theme.

        Parameters
        ----------
        metadata : ScheduleMetadata
            An instance of `ScheduleMetadata`
            containing the title, authors,
            abstracts, and anthology URLs for
            each item, if applicable.
        paper_icons : bool, optional
            Whether to generate the icons for
            each of the presentation items linked
            to the PDF on the anthology.
            Defaults to `False`.
        video_icons : bool, optional
            Whether to generate the icons for
            each of the oral presentation items
            linked to the video of the talk.
            Defaults to `False`.

        Returns
        -------
        item_html : str
            A string containing the item HTML.

        """

        # initialize the result variable
        generated_html = []

        # generate the appropriate type of HTML depending on item type
        if self.type == 'paper':
            self.title = metadata[self.id_].title
            self.authors = metadata[self.id_].authors
            self.paper_url = metadata[self.id_].anthology_url
            item_html = '<tr id="paper" paper-id="{}"><td id="paper-time">{}&ndash;{}</td><td><span class="paper-title">{}. </span><em>{}</em>'.format(self.id_, self.start, self.end, self.title, self.authors)
            if paper_icons:
                item_html += '&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="{}" aria-hidden="true" title="PDF"></i>'.format(self.paper_url)
            if video_icons:
                item_html += '&nbsp;<i class="fa fa-file-video-o video-icon" data="{}" aria-hidden="true" title="Video"></i>'.format(self.video_url)
            item_html += '</td></tr>'
            generated_html.append(item_html)

        elif self.type == 'poster':
            self.title = metadata[self.id_].title
            self.authors = metadata[self.id_].authors
            self.paper_url = metadata[self.id_].anthology_url
            if self.topic:
                generated_html.append('<tr><td><span class="poster-type">{}</span></td></tr>'.format(self.topic))
            item_html = '<tr id="poster" poster-id="{}"><td><span class="poster-title">{}. </span><em>{}</em>'.format(self.id_, self.title, self.authors)
            if paper_icons:
                item_html += '&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="{}" aria-hidden="true" title="PDF"></i>'.format(self.paper_url)
            item_html += '</td></tr>'
            generated_html.append(item_html)

        elif self.type == 'tutorial':
            self.title = metadata[self.id_].title
            self.authors = metadata[self.id_].authors
            generated_html.append('<tr id="tutorial"><td><span class="tutorial-title"><strong>{}. </strong>{}. </span><br/><span class="btn btn--location inline-location">{}</span></td></tr>'.format(self.title, self.authors, self.location))

        # return the generated item HTML
        return generated_html


def main():

    # set up an argument parser
    parser = argparse.ArgumentParser(prog='webschedule.py')
    parser.add_argument("--order",
                        dest="orderfile",
                        required=True,
                        help="Manually combined order file")
    parser.add_argument("--xmls",
                        dest="xml_files",
                        required=True,
                        nargs='+',
                        type=Path,
                        help="Anthology XML files containing author "
                             "and title metadata")
    parser.add_argument("--mappings",
                        dest="mapping_files",
                        required=True,
                        nargs='+',
                        type=Path,
                        help="Files mapping order Anthology IDs "
                             "to order file IDs.")
    parser.add_argument("--extra-metadata",
                        dest="extra_metadata_file",
                        required=False,
                        default=None,
                        type=Path,
                        help="TSV file containing authors and "
                             "titles not in anthology XMLs")
    parser.add_argument("--output",
                        dest="output_file",
                        required=True,
                        help="Output markdown file")
    parser.add_argument("--paper-icons",
                        action="store_true",
                        default=False,
                        dest="paper_icons",
                        required=False,
                        help="Generate icons linking "
                             "to anthology PDFs")
    parser.add_argument("--video-icons",
                        action="store_true",
                        default=False,
                        dest="video_icons",
                        required=False,
                        help="Generate icons linking "
                             "to talk videos")

    # parse given command line arguments
    args = parser.parse_args()

    # set up the logging
    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

    # parse the orderfile into a `WebAgenda` object
    logging.info('Parsing order file ...')
    wa = WebAgenda()
    wa.fromfile(args.orderfile)

    # parse the metadata files
    logging.info('Parsing metadata files ...')
    metadata = ScheduleMetadata.fromfiles(xmls=args.xml_files,
                                          mappings=args.mapping_files,
                                          non_anthology_tsv=args.extra_metadata_file)
    # convert WebAgenda to HTML
    logging.info("Converting parsed agenda to HTML ...")
    html = wa.to_html(metadata,
                      paper_icons=args.paper_icons,
                      video_icons=args.video_icons)

    # add the Jekyll frontmatter
    logging.info("Adding Jekyll frontmatter ...")
    frontmatter = open(_THIS_DIR / 'frontmatter.md', 'r').read()
    final_page_content = '\n'.join([frontmatter, html])

    # write out the content to the output file
    logging.info('Writing content to output file ...')
    with open(args.output_file, 'w') as outputfh:
        outputfh.write(final_page_content)


if __name__ == '__main__':
    main()
