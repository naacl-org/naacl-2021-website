---
title: Conference Schedule
layout: schedule
excerpt: "NAACL 2019 conference schedule."
permalink: /schedule
sidebar: false
script: |
    <script type="text/javascript">

        sessionInfoHash = {};
        paperInfoHash = {};
        chosenPapersHash = {};
        chosenTutorialsHash = {};
        chosenWorkshopsHash = {};
        chosenPostersHash = {};
        plenarySessionHash = {};
        includePlenaryInSchedule = true;
        helpShown = false;

        var instructions = "<div id=\"popupInstructionsDiv\"><div id=\"title\">Help</div><div id=\"popupInstructions\"><ul><li>Click on a the \"<strong>+</strong>\" button or the title of a session to toggle it. Click the <strong>\"Expand All Sessions ↓\"</strong> button to expand <em>all</em> sessions in one go. Click again to collapse them. </li> <li>Click on a tutorial/paper/poster to toggle its selection. </li> <li>You can select more than one paper for a time slot. </li> <li>Click the &nbsp;<i class=\"fa fa-file-pdf-o\" aria-hidden=\"true\"></i>&nbsp; /&nbsp;<i class=\"fa fa-file-video-o\" aria-hidden=\"true\"></i>&nbsp; icon(s) for the PDF / Video. </li> <li>Click the <strong>\"Download PDF\"</strong> button at the bottom to download your customized PDF. </li> <li>To expand parallel sessions simultaneously, hold Shift and click on any of them. </li> <li>On non-mobile devices, hovering on a paper for a time slot highlights it in yellow and its conflicting papers in red. Hovering on papers already selected for a time slot (or their conflicts) highlights them in green. </li> <li>Hover over the time for any session to see its day and date as a tooltip.</li> <li>While saving the generated PDF on mobile devices, its name cannot be changed.</li> </ul></div></div>";

        function padTime(str) {
            return String('0' + str).slice(-2);
        }

        function formatDate(dateObj) {
            return dateObj.toLocaleDateString() + ' ' + padTime(dateObj.getHours()) + ':' + padTime(dateObj.getMinutes());
        }

        function generatePDFfromTable() {

            /* clear the hidden table before starting */
            clearHiddenProgramTable();

            /* now populate the hidden table with the currently chosen papers */
            populateHiddenProgramTable();

            var doc = new jsPDF('l', 'pt', 'letter');
            doc.autoTable({
                fromHtml: "#hidden-program-table",
                pagebreak: 'avoid',
                avoidRowSplit: true,
                theme: 'grid',
                startY: 70, 
                showHead: false,
                styles: {
                    font: 'times',
                    overflow: 'linebreak',
                    valign: 'middle',
                    lineWidth: 0.4,
                    fontSize: 11
                },
                 columnStyles: {
                    0: { fontStyle: 'bold', halign: 'right', cellWidth: 70 },
                    1: { cellWidth: 110 },
                    2: { fontStyle: 'italic', cellWidth: 530 }
                },
                addPageContent: function (data) {
                    /* HEADER only on the first page */
                    var pageNumber = doc.internal.getCurrentPageInfo().pageNumber;

                    if (pageNumber == 1) {
                        doc.setFontSize(16);
                        doc.setFontStyle('normal');
                        doc.text("NAACL 2019 Schedule", (doc.internal.pageSize.width - (data.settings.margin.left*2))/2 - 30, 50);
                    }

                    /* FOOTER on each page */
                    doc.setFont('courier');
                    doc.setFontSize(8);
                    doc.text('(Generated via https://naacl2019.org/schedule)', data.settings.margin.left, doc.internal.pageSize.height - 10);
                },
                drawCell: function(cell, data) {
                    var cellClass = cell.raw.content.className;
                    /* center the day header */
                    if (cellClass == 'info-day') {
                        cell.textPos.x = (530 - data.settings.margin.left)/2 + 120;
                    }
                    /* split long plenary session text */
                    else if (cellClass == 'info-plenary') {
                        cell.text = doc.splitTextToSize(cell.text.join(' '), 530, {fontSize: 11});
                    }
                },
                createdCell: function(cell, data) {
                    var cellClass = cell.raw.content.className;
                    var cellText = cell.text[0];
                    /* */
                    if (cellClass == 'info-day') {
                        cell.styles.fontStyle = 'bold';
                        cell.styles.fontSize = 12;
                        cell.styles.fillColor = [187, 187, 187];
                    }
                    else if (cellClass == 'info-plenary') {
                        cell.styles.fontSize = 11;
                        if (cellText.search(/break|lunch|breakfast/i) !== -1) {
                            cell.styles.fillColor = [238, 238, 238];
                        }
                    }
                    else if (cellClass == 'info-poster') {
                        cell.styles.fontSize = 9;
                    }
                    else if (cellClass == "location") {
                        if (cellText == '') {
                            var infoType = data.row.raw[2].content.className;
                            if (infoType == "info-day") {
                                cell.styles.fillColor = [187, 187, 187];
                            }
                            else if (infoType == "info-plenary") {
                                cell.styles.fillColor = [238, 238, 238];
                            }
                        }
                    }
                    else if (cellClass == "time") {
                        var infoType = data.row.raw[2].content.className;
                        var infoText = data.row.raw[2].content.textContent;
                        if (infoType == "info-day" && cellText == '') {
                            cell.styles.fillColor = [187, 187, 187];
                        }
                        if (infoType == "info-plenary" &&  infoText.search(/(break|lunch|breakfast)/i) !== -1) {
                            cell.styles.fillColor = [238, 238, 238];
                        }
                    }
                },
            });
            doc.output('save');
        }

        function getTutorialInfoFromTime(tutorialTimeObj) {

            /* get the tutorial session and day */
            var tutorialSession = tutorialTimeObj.parents('.session');
            var sessionDay = tutorialSession.prevAll('.day:first').text().trim();

            /* get the tutorial slot and the starting and ending times */
            var tutorialTimeText = tutorialTimeObj.text().trim();
            var tutorialTimes = tutorialTimeText.split(' ');
            var tutorialSlotStart = tutorialTimes[0];
            var tutorialSlotEnd = tutorialTimes[2];
            var exactTutorialStartingTime = sessionDay + ' ' + tutorialSlotStart;
            return [new Date(exactTutorialStartingTime).getTime(), tutorialSlotStart, tutorialSlotEnd, tutorialSession.attr('id')];
        }

        function getWorkshopInfoFromTime(workshopTimeObj) {

            /* get the workshop session and day */
            var workshopSession = workshopTimeObj.parents('.session');
            var sessionDay = workshopSession.prevAll('.day:first').text().trim();

            /* get the workshop slot and the starting and ending times */
            var workshopTimeText = workshopTimeObj.text().trim();
            var workshopTimes = workshopTimeText.split(' ');
            var workshopSlotStart = workshopTimes[0];
            var workshopSlotEnd = workshopTimes[2];
            var exactworkshopStartingTime = sessionDay + ' ' + workshopSlotStart;
            return [new Date(exactworkshopStartingTime).getTime(), workshopSlotStart, workshopSlotEnd, workshopSession.attr('id')];
        }

        function getPosterInfoFromTime(posterTimeObj) {

            /* get the poster session and day */
            var posterSession = posterTimeObj.parents('.session');
            var sessionDay = posterSession.parent().prevAll('.day:first').text().trim();

            /* get the poster slot and the starting and ending times */
            var posterTimeText = posterTimeObj.text().trim();
            var posterTimes = posterTimeText.split(' ');
            var posterSlotStart = posterTimes[0];
            var posterSlotEnd = posterTimes[2];
            var exactPosterStartingTime = sessionDay + ' ' + posterSlotStart;
            return [new Date(exactPosterStartingTime).getTime(), posterSlotStart, posterSlotEnd, posterSession.attr('id')];
        }

        function isOverlapping(thisPaperRange, otherPaperRange) {
            var thisStart = thisPaperRange[0];
            var thisEnd = thisPaperRange[1];
            var otherStart = otherPaperRange[0];
            var otherEnd = otherPaperRange[1];
            return ((thisStart < otherEnd) && (thisEnd > otherStart));
        }

        function getConflicts(paperObject) {

            /* first get the parallel sessions */
            var sessionId = paperObject.parents('.session').attr('id').match(/session-\d/)[0];
            var parallelSessions = paperObject.parents('.session').siblings().filter(function() { return this.id.match(sessionId); });
            
            var thisPaperRange = paperInfoHash[paperObject.attr('paper-id')].slice(0, 2);
            return $(parallelSessions).find('table.paper-table tr#paper').filter(function(index) {
                    var otherPaperRange =  paperInfoHash[$(this).attr('paper-id')].slice(0, 2);
                    return isOverlapping(thisPaperRange, otherPaperRange) 
                });
        }

        function doWhichKey(e) {
            e = e || window.event;
            var charCode = e.keyCode || e.which;
            //Line below not needed, but you can read the key with it
            //var charStr = String.fromCharCode(charCode);
            return charCode;
        }

        function getConflicts2(paperObject) {

            /* most of the time, conflicts are simply based on papers having the same exact time slot but this is not always true */

            /* first get the conflicting sessions */
            var sessionId = paperObject.parents('.session').attr('id').match(/session-\d/)[0];
            var parallelSessions = paperObject.parents('.session').siblings().filter(function() { return this.id.match(sessionId); });
            
            /* now get the conflicting papers from those sessions */
            var paperTime = paperObject.children('td#paper-time')[0].textContent;
            return $(parallelSessions).find('table.paper-table tr#paper').filter(function(index) { return this.children[0].textContent == paperTime });

        }

        function makeDayHeaderRow(day) {
            return '<tr><td class="time"></td><td class="location"></td><td class="info-day">' + day + '</td></tr>';
        }

        function makePlenarySessionHeaderRow(session) {
            var sessionStart = session.start;
            var sessionEnd = session.end;
            return '<tr><td class="time">' + sessionStart + '&ndash;' + sessionEnd + '</td><td class="location">' + session.location + '</td><td class="info-plenary">' + session.title + '</td></tr>';
        }

        function makePaperRows(start, end, titles, sessions) {
            var ans;
            if (titles.length == 1) {
                ans = ['<tr><td class="time">' + start + '&ndash;' + end + '</td><td class="location">' + sessions[0].location + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
            }
            else {
                var numConflicts = titles.length;
                rows = ['<tr><td rowspan=' + numConflicts + ' class="time">' + start + '&ndash;' + end + '</td><td class="location">' + sessions[0].location + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
                for (var i=1; i<numConflicts; i++) {
                    var session = sessions[i];
                    var title = titles[i];
                    rows.push('<tr><td></td><td class="location">' + session.location + '</td><td class="info-paper">' + title + ' [' + session.title + ']</td></tr>')
                }
                ans = rows;
            }
            return ans;
        }

        function makeTutorialRows(start, end, titles, locations, sessions) {
            var ans;
            if (titles.length == 1) {
                ans = ['<tr><td class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
            }
            else {
                var numConflicts = titles.length;
                rows = ['<tr><td rowspan=' + numConflicts + ' class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
                for (var i=1; i<numConflicts; i++) {
                    var session = sessions[i];
                    var title = titles[i];
                    var location = locations[i];
                    rows.push('<tr><td></td><td class="location">' + location + '</td><td class="info-paper">' + title + ' [' + session.title + ']</td></tr>')
                }
                ans = rows;
            }
            return ans;
        }

    function makeWorkshopRows(start, end, titles, locations, sessions) {
            var ans;
            if (titles.length == 1) {
                ans = ['<tr><td class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
            }
            else {
                var numConflicts = titles.length;
                rows = ['<tr><td rowspan=' + numConflicts + ' class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
                for (var i=1; i<numConflicts; i++) {
                    var session = sessions[i];
                    var title = titles[i];
                    var location = locations[i];
                    rows.push('<tr><td></td><td class="location">' + location + '</td><td class="info-paper">' + title + ' [' + session.title + ']</td></tr>')
                }
                ans = rows;
            }
            return ans;
        }

        function makePosterRows(titles, types, sessions) {
            var numPosters = titles.length;
            var sessionStart = sessions[0].start;
            var sessionEnd = sessions[0].end;
            rows = ['<tr><td rowspan=' + (numPosters + 1) + ' class="time">' + sessionStart + '&ndash;' + sessionEnd + '</td><td rowspan=' + (numPosters + 1) + ' class="location">' + sessions[0].location + '</td><td class="info-paper">' + sessions[0].title +  '</td></tr>'];
            for (var i=0; i<numPosters; i++) {
                var title = titles[i];
                var type = types[i];
                /* rows.push('<tr><td></td><td></td><td class="info-poster">' + title + ' [' + type + ']</td></tr>'); */
                rows.push('<tr><td></td><td></td><td class="info-poster">' + title + '</td></tr>');
            }
            return rows;
        }

        function clearHiddenProgramTable() {
            $('#hidden-program-table tbody').html('');
        }

        function getChosenHashFromType(type) {
            var chosenHash;
            if (type == 'paper') {
                chosenHash = chosenPapersHash;
            }
            else if (type == 'tutorial') {
                chosenHash = chosenTutorialsHash;
            }
            else if (type == 'workshop') {
                chosenHash = chosenWorkshopsHash;
            }
            else if (type == 'poster') {
                chosenHash = chosenPostersHash;
            }
            return chosenHash;
        }

        function addToChosen(timeKey, item, type) {
            var chosenHash = getChosenHashFromType(type);
            if (timeKey in chosenHash) {
                var items = chosenHash[timeKey];
                items.push(item);
                chosenHash[timeKey] = items;
            }
            else {
                chosenHash[timeKey] = [item];
            }
        }

        function removeFromChosen(timeKey, item, type) {
            var chosenHash = getChosenHashFromType(type);            
            if (timeKey in chosenHash) {
                var items = chosenHash[timeKey];
                var itemIndex = items.map(function(item) { return item.title; }).indexOf(item.title);
                if (itemIndex !== -1) {
                    var removedItem = items.splice(itemIndex, 1);
                    delete removedItem;
                    if (items.length == 0) {
                        delete chosenHash[timeKey];
                    }
                    else {
                        chosenHash[timeKey] = items;
                    }
                }
            }
        }

        function isChosen(timeKey, item, type) {
            var ans = false;
            var chosenHash = getChosenHashFromType(type);
            if (timeKey in chosenHash) {
                var items = chosenHash[timeKey];
                var itemIndex = items.map(function(item) { return item.title; }).indexOf(item.title);
                ans = itemIndex !== -1;
            }
            return ans;
        }

        function toggleSession(sessionObj) {
            $(sessionObj).children('[class$="-details"]').slideToggle(300);
            $(sessionObj).children('#expander').toggleClass('expanded');
        }

        function openSession(sessionObj) {
            $(sessionObj).children('[class$="-details"]').slideDown(300);
            $(sessionObj).children('#expander').addClass('expanded');
        }

        function closeSession(sessionObj) {
            $(sessionObj).children('[class$="-details"]').slideUp(300);
            $(sessionObj).children('#expander').removeClass('expanded');
        }

        function populateHiddenProgramTable() {

            /* since papers and posters might start at the same time we cannot just rely on starting times to differentiate papers vs. posters. so, what we can do is just add an item type after we do the concatenation and then rely on that item type to distinguish the item */
            
            var nonPlenaryKeysAndTypes = [];
            var tutorialKeys = Object.keys(chosenTutorialsHash);
            var workshopKeys = Object.keys(chosenWorkshopsHash);
            var posterKeys = Object.keys(chosenPostersHash);
            var paperKeys = Object.keys(chosenPapersHash);
            for (var i=0; i < tutorialKeys.length; i++) {
                nonPlenaryKeysAndTypes.push([tutorialKeys[i], 'tutorial']);
            }
            for (var i=0; i < workshopKeys.length; i++) {
                nonPlenaryKeysAndTypes.push([workshopKeys[i], 'workshop']);
            }
            for (var i=0; i < posterKeys.length; i++) {
                nonPlenaryKeysAndTypes.push([posterKeys[i], 'poster']);
            }
            for (var i=0; i < paperKeys.length; i++) {
                nonPlenaryKeysAndTypes.push([paperKeys[i], 'paper']);
            }

            var plenaryKeys = Object.keys(plenarySessionHash);
            var plenaryKeysAndTypes = [];
            for (var i=0; i < plenaryKeys.length; i++) {
                plenaryKeysAndTypes.push([plenaryKeys[i], 'plenary']);
            }

            /* if we are including plenary information in the PDF then sort its keys too and merge the two sets of keys together before sorting */
            var sortedPaperTimes = includePlenaryInSchedule ? nonPlenaryKeysAndTypes.concat(plenaryKeysAndTypes) : nonPlenaryKeysAndTypes;
            sortedPaperTimes.sort(function(a, b) { return a[0] - b[0] });

            /* now iterate over these sorted papers and create the rows for the hidden table that will be used to generate the PDF */
            var prevDay = null;
            var latestEndingTime;
            var output = [];

            /* now iterate over the chosen items */
            for(var i=0; i<sortedPaperTimes.length; i++) {
                var keyAndType = sortedPaperTimes[i];
                var key = keyAndType[0];
                var itemType = keyAndType[1]
                /* if it's a plenary session */
                if (itemType == 'plenary') {
                    var plenarySession = plenarySessionHash[key];
                    if (plenarySession.day == prevDay) {
                        output.push(makePlenarySessionHeaderRow(plenarySession));
                    }
                    else {
                        output.push(makeDayHeaderRow(plenarySession.day));
                        output.push(makePlenarySessionHeaderRow(plenarySession));
                    }
                    prevDay = plenarySession.day;
                }
                /* if it's tutorials */
                else if (itemType == 'tutorial') {

                    /* get the tutorials */
                    var tutorials = chosenTutorialsHash[key];

                    /* sort the tutorials by title instead of selection order */
                    tutorials.sort(function(a, b) {
                        return a.title.localeCompare(b.title);
                    });

                    var titles = tutorials.map(function(tutorial) { return ASCIIFold(tutorial.title); });
                    var locations = tutorials.map(function(tutorial) { return tutorial.location ; });
                    var sessions = tutorials.map(function(tutorial) { return sessionInfoHash[tutorial.session]; });
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makeTutorialRows(tutorials[0].start, tutorials[0].end, titles, locations, sessions));
                    prevDay = sessionDay;
                }
                /* if it's workshops */
                else if (itemType == 'workshop') {

                    /* get the workshops */
                    var workshops = chosenWorkshopsHash[key];

                    /* sort the workshops by title instead of selection order */
                    workshops.sort(function(a, b) {
                        return a.title.localeCompare(b.title);
                    });

                    var titles = workshops.map(function(workshop) { return ASCIIFold(workshop.title); });
                    var locations = workshops.map(function(workshop) { return workshop.location ; });
                    var sessions = workshops.map(function(workshop) { return sessionInfoHash[workshop.session]; });
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makeWorkshopRows(workshops[0].start, workshops[0].end, titles, locations, sessions));
                    prevDay = sessionDay;
                }
                /* if it's posters */
                else if (itemType == 'poster') {

                    /* get the posters */
                    var posters = chosenPostersHash[key];

                    /* sort posters by their type for easier reading */
                    posters.sort(function(a, b) {
                        return a.type.localeCompare(b.type);
                    });
                    var titles = posters.map(function(poster) { return ASCIIFold(poster.title); });
                    var types = posters.map(function(poster) { return poster.type; });
                    var sessions = [sessionInfoHash[posters[0].session]];
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makePosterRows(titles, types, sessions));
                    prevDay = sessionDay;
                }

                /* if it's papers  */
                else if (itemType == 'paper') {
                    var papers = chosenPapersHash[key];
                    /* sort papers by location for easier reading */
                    papers.sort(function(a, b) {
                        var aLocation = sessionInfoHash[a.session].location;
                        var bLocation = sessionInfoHash[b.session].location;
                        return aLocation.localeCompare(bLocation);
                    });
                    var titles = papers.map(function(paper) { return ASCIIFold(paper.title); });
                    var sessions = papers.map(function(paper) { return sessionInfoHash[paper.session]; });
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makePaperRows(papers[0].start, papers[0].end, titles, sessions));
                    prevDay = sessionDay;
                }
            }

            /* append the output to the hidden table */
            $('#hidden-program-table tbody').append(output);
        }

        $(document).ready(function() {
            
            /* all the Remove All buttons are disabled on startup */
            $('.session-deselector').addClass('disabled');

            /* the include plenary checkbox is checked on startup */
            $('input#includePlenaryCheckBox').prop('checked', true);

            /* show the help window whenever "?" is pressed */
            $(document).keypress(function(event) {
                if (doWhichKey(event) == 63 && !helpShown) {
                    helpShown = true;
                    alertify.alert(instructions, function(event) { helpShown = false;});
                }
            });

            /* show the help window when the help button is clicked */
            $('a#help-button').on('click', function (event) {
                if (!helpShown) {
                    event.preventDefault();
                    helpShown = true;
                    alertify.alert(instructions, function(event) { helpShown = false;});
                }
            });

            /* expand/collapse all sessions when the toggle button is clicked */
            $('a#toggle-all-button').on('click', function (event) {
                event.preventDefault();
                var buttonText = $(this).text();

                / * expand all collapsed sessions */
                if (buttonText == 'Expand All Sessions ↓') {
                    $('div#expander').not('.expanded').trigger('click');
                    $(this).text('Collapse All Sessions ↑');
                }
                /* collapse all expanded sessions */
                else {
                    $('div#expander.expanded').trigger('click');
                    $(this).text('Expand All Sessions ↓');
                }
            });


            $('span.session-location, span.inline-location').on('click', function(event) {
                event.stopPropagation();
            });

            $('span.session-external-location').on('click', function(event) {
                var placeName = $(this).text().trim().replace(" ", "+");
                window.open("https://www.google.com/maps?q=" + placeName, "_blank");
                event.stopPropagation();
            });

            /* show the floorplan when any location is clicked */
            $('span.session-location, span.inline-location').magnificPopup({
                items: {
                    src: '/assets/images/minneapolis/3d-floormap.png'
                },
                type: 'image',
                fixedContentPos: 'auto'
            });

            /* get all the tutorial sessions and save the day and location for each of them in a hash */
            $('.session-tutorials').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.day = $(this).prevAll('.day:first').text().trim();
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* get all the workshop sessions and save the day and location for each of them in a hash */
            $('.session-workshops').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.day = $(this).prevAll('.day:first').text().trim();
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* get all the poster sessions and save the day and location for each of them in a hash */
            $('.session-posters').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.day = $(this).parent().prevAll('.day:first').text().trim();
                session.location = $(this).children('span.session-location').text().trim();
                var sessionTimeText = $(this).children('span.session-time').text().trim();                
                var sessionTimes = sessionTimeText.match(/\d+:\d+/g);
                var sessionStart = sessionTimes[0];
                var sessionEnd = sessionTimes[1];
                session.start = sessionStart;
                session.end = sessionEnd;
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* get all the paper sessions and save the day and location for each of them in a hash */
            var paperSessions = $("[id|='session']").filter(function() { 
                return this.id.match(/session-\d\d?[a-z]$/);
            });
            $(paperSessions).each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.location = $(this).children('span.session-location').text().trim();
                session.day = $(this).parent().prevAll('.day:first').text().trim();
                var sessionTimeText = $(this).children('span.session-time').text().trim();                
                var sessionTimes = sessionTimeText.match(/\d+:\d+/g);
                var sessionStart = sessionTimes[0];
                var sessionEnd = sessionTimes[1];
                session.start = sessionStart;
                session.end = sessionEnd;
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* iterate over all the papers and store all their info in a hash since we need that info whenever we click and hover and lookups will be faster than re-computing the info at each event */
            $('tr#paper').each(function() {
                var paperID = $(this).attr('paper-id');

                /* get the paper session and day */
                var paperSession = $(this).parents('.session');
                var sessionDay = paperSession.parent().prevAll('.day:first').text().trim();

                /* get the paper time and title */
                var paperTimeObj = $(this).children('#paper-time');
                var paperTitle = paperTimeObj.siblings('td').text().trim().replace(/\s\s+/g, " ");

                /* get the paper slot and the starting and ending times */
                var paperTimeText = paperTimeObj.text().trim();
                var paperTimes = paperTimeText.split('\u2013');
                var paperSlotStart = paperTimes[0];
                var paperSlotEnd = paperTimes[1];
                var exactPaperStartingTime = sessionDay + ' ' + paperSlotStart;
                var exactPaperEndingTime = sessionDay + ' ' + paperSlotEnd;

                paperInfoHash[paperID] = [new Date(exactPaperStartingTime).getTime(), new Date(exactPaperEndingTime).getTime(), paperSlotStart, paperSlotEnd, paperTitle, paperSession.attr('id')];
            });

            /* also save the plenary session info in another hash since we may need to add this to the pdf. Use the exact starting time as the hash key */
             $('.session-plenary').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                if (session.title == "Social Event") {
                    session.location = $(this).children('span.session-external-location').text().trim();
                }
                else {
                    session.location = $(this).children('span.session-location').text().trim();                    
                }
                session.day = $(this).prevAll('.day:first').text().trim();
                session.id = $(this).attr('id');
                var sessionTimeText = $(this).children('span.session-time').text().trim();
                var sessionTimes = sessionTimeText.match(/\d+:\d+/g);
                var sessionStart = sessionTimes[0];
                var sessionEnd = sessionTimes[1];
                session.start = sessionStart;
                session.end = sessionEnd;
                var exactSessionStartingTime = session.day + ' ' + sessionStart;
                plenarySessionHash[new Date(exactSessionStartingTime).getTime()] = session;
             });

            $('body').on('click', 'a.session-selector', function(event) {

                /* if we are disabled, do nothing */
                if ($(this).hasClass('disabled')) {
                    return false;
                }

                /* if we are choosing the entire session, then basically "click" on all of the not-selected papers */
                var sessionPapers = $(this).siblings('table.paper-table').find('tr#paper');
                var unselectedPapers = sessionPapers.not('.selected');
                unselectedPapers.trigger('click', true);

                /* now find out how many papers are selected after the trigger */
                var selectedPapers = sessionPapers.filter('.selected');

                /* disable myself (the choose all button) */
                $(this).addClass('disabled');

                /* if we didn't have any papers selected earlier, then enable the remove all button */
                if (unselectedPapers.length == sessionPapers.length) {
                    $(this).siblings('.session-deselector').removeClass('disabled');
                }

                /* this is not really a link */
                event.preventDefault();
                return false;
            });

            $('body').on('click', 'a.session-deselector', function(event) {

                /* if we are disabled, do nothing */
                if ($(this).hasClass('disabled')) {
                    return false;
                }

                /* otherwise, if we are removing the entire session, then basically "click" on all of the already selected papers */
                var sessionPapers = $(this).siblings('table.paper-table').find('tr#paper');
                var selectedPapers = sessionPapers.filter('.selected');
                selectedPapers.trigger('click', true);

                /* disable myself (the remove all button) */
                $(this).addClass('disabled');

                /* enable the choose all button */
                $(this).siblings('session-deselector').removeClass('disabled');

                /* if all the papers were selected earlier, then enable the choose all button */
                if (selectedPapers.length == sessionPapers.length) {
                    $(this).siblings('.session-selector').removeClass('disabled');                    
                }

                /* this is not really a link */
                event.preventDefault();
                return false;
            });

            /* hide all of the session details when starting up */
            $('[class$="-details"]').hide();

            /* expand sessions when their title is clicked */
            $('body').on('click', 'div.session-expandable .session-title, div#expander', function(event) {
                event.preventDefault();
                event.stopPropagation();
                var sessionObj = $(this).parent();

                /* if we had the shift key pressed, then expand ALL unexpanded parallel sessions including myself (only for papers) */
                if (event.shiftKey && sessionObj.attr('class').match('session-papers')) {
                    var sessionId = $(sessionObj).attr('id').match(/session-\d/)[0];
                    var parallelSessions = $(sessionObj).siblings().addBack().filter(function() { return this.id.match(sessionId); });

                    var unexpandedParallelSessions = $(parallelSessions).filter(function() { return !$(this).children('#expander').hasClass('expanded'); });

                    /* if all sessions are already expanded, then shift-clicking should close all of them */
                    if (unexpandedParallelSessions.length == 0) {
                        $.map(parallelSessions, closeSession);
                    }
                    else {
                        $.map(unexpandedParallelSessions, openSession);
                    }
                } 
                /* for a regular click, just toggle the individual session */
                else {
                    toggleSession(sessionObj);
                }
            });

            /* when we mouse over a paper icon, do not do anything */
            $('body').on('mouseover', 'table.paper-table tr#paper i[class$="-icon"]', function(event) {
                return false;
            });

            /* when we mouse over a paper, highlight the conflicting papers */
            $('body').on('mouseover', 'table.paper-table tr#paper', function(event) {
                var conflictingPapers = getConflicts($(this));
                $(this).addClass('hovered');
                $(conflictingPapers).addClass('conflicted');
            });

            /* when we mouse out, remove all highlights */
            $('body').on('mouseout', 'table.paper-table tr#paper', function(event) {
                var conflictingPapers = getConflicts($(this));
                $(this).removeClass('hovered');
                $(conflictingPapers).removeClass('conflicted');

            });

            $('body').on('click', 'a.info-button', function(event) {
                return false;
            });

            $('body').on('click', 'a.info-link', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'div.session-abstract', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'table.paper-table', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'table.tutorial-table', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'table.poster-table', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'div.paper-session-details', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'input#includePlenaryCheckBox', function(event) {
                    includePlenaryInSchedule = $(this).prop('checked');
            });

            $('body').on('click', 'a#generatePDFButton', function(event) {
                /* if we haven't chosen any papers, and we aren't including plenary sessions either, then raise an error. If we are including plenary sessions and no papers, then confirm. */
                event.preventDefault();
                var numChosenItems = Object.keys(chosenPapersHash).length + Object.keys(chosenTutorialsHash).length + Object.keys(chosenWorkshopsHash).length + Object.keys(chosenPostersHash).length;
                if (numChosenItems == 0) {
                    if (includePlenaryInSchedule) {
                        alertify.confirm("The PDF will contain only the plenary sessions since nothing was chosen. Proceed?", function () { generatePDFfromTable();
                                }, function() { return false; });
                    }
                    else {
                        alertify.alert('Nothing to generate. Nothing was chosen and plenary sessions were excluded.');
                        return false;
                    }
                }
                else {
                    generatePDFfromTable();
                }
            });

            $('body').on('click', 'table.tutorial-table tr#tutorial', function(event) {
                event.preventDefault();
                var tutorialTimeObj = $(this).parents('.session-tutorials').children('.session-time');
                var tutorialInfo = getTutorialInfoFromTime(tutorialTimeObj);
                var tutorialObject = {};
                var exactStartingTime = tutorialInfo[0];
                tutorialObject.start = tutorialInfo[1];
                tutorialObject.end = tutorialInfo[2];
                tutorialObject.title = $(this).find('.tutorial-title').text();
                tutorialObject.session = tutorialInfo[3];
                tutorialObject.location = $(this).find('.inline-location').text();
                tutorialObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected tutorial */
                if (isChosen(exactStartingTime, tutorialObject, 'tutorial')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, tutorialObject, 'tutorial');
                }
                else {
                    addToChosen(exactStartingTime, tutorialObject, 'tutorial');
                    $(this).addClass('selected');                    
                }
            });

            $('body').on('click', 'table.workshop-table tr#workshop', function(event) {
                event.preventDefault();
                var workshopTimeObj = $(this).parents('.session-workshops').children('.session-time');
                var workshopInfo = getWorkshopInfoFromTime(workshopTimeObj);
                var workshopObject = {};
                var exactStartingTime = workshopInfo[0];
                workshopObject.start = workshopInfo[1];
                workshopObject.end = workshopInfo[2];
                workshopObject.title = $(this).find('.workshop-title').text();
                workshopObject.session = workshopInfo[3];
                workshopObject.location = $(this).find('.inline-location').text();
                workshopObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected workshop */
                if (isChosen(exactStartingTime, workshopObject, 'workshop')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, workshopObject, 'workshop');
                }
                else {
                    addToChosen(exactStartingTime, workshopObject, 'workshop');
                    $(this).addClass('selected');                    
                }
            });

            $('body').on('click', 'table.poster-table tr#poster', function(event) {
                event.preventDefault();
                var posterTimeObj = $(this).parents('.session-posters').children('.session-time');
                var posterInfo = getPosterInfoFromTime(posterTimeObj);
                var posterObject = {};
                var exactStartingTime = posterInfo[0];
                posterObject.start = posterInfo[1];
                posterObject.end = posterInfo[2];
                posterObject.title = $(this).find('.poster-title').text().trim();
                posterObject.type = $(this).parents('.poster-table').prevAll('.poster-type:first').text().trim();
                posterObject.session = posterInfo[3];
                posterObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected poster */
                if (isChosen(exactStartingTime, posterObject, 'poster')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, posterObject, 'poster');
                }
                else {
                    addToChosen(exactStartingTime, posterObject, 'poster');
                    $(this).addClass('selected');
                    var key = new Date(exactStartingTime).getTime();
                    if (key in plenarySessionHash) {
                        delete plenarySessionHash[key];
                    }
                }
            });

            /* open the URL in a new window/tab when we click on the any icon - whether it is the keynote slides or the video */            
            $('body').on('click', 'div.session-abstract p i[class$="-icon"]', function(event) {
                event.stopPropagation();
                event.preventDefault();
                var urlToOpen = $(this).attr('data');
                if (urlToOpen !== '') {
                    window.open(urlToOpen, "_blank");
                }
            });


            /* open the anthology or video URL in a new window/tab when we click on the PDF or video icon respectively  */            
            $('body').on('click', 'table.tutorial-table tr#tutorial i[class$="-icon"],table.paper-table tr#paper i[class$="-icon"],table.paper-table tr#best-paper i[class$="-icon"],table.poster-table tr#poster i[class$="-icon"]', function(event) {
                event.stopPropagation();
                event.preventDefault();
                var urlToOpen = $(this).attr('data');
                if (urlToOpen !== '') {
                    window.open(urlToOpen, "_blank");
                }
            });

            $('body').on('click', 'table.paper-table tr#paper', function(event, fromSession) {
                event.preventDefault();
                $(this).removeClass('hovered');
                getConflicts($(this)).removeClass('conflicted');
                var paperID = $(this).attr('paper-id');
                var paperTimeObj = $(this).children('td#paper-time');
                var paperInfo = paperInfoHash[paperID];
                var paperObject = {};
                var exactStartingTime = paperInfo[0];
                paperObject.start = paperInfo[2];
                paperObject.end = paperInfo[3];
                paperObject.title = paperInfo[4];
                paperObject.session = paperInfo[5];
                paperObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected paper */
                if (isChosen(exactStartingTime, paperObject, 'paper')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, paperObject, 'paper');

                    /* if we are not being triggered at the session level, then we need to handle the state of the session level button ourselves */
                    if (!fromSession) {
        
                        /* we also need to enable the choose button */
                        $(this).parents('table.paper-table').siblings('.session-selector').removeClass('disabled');

                        /* we also need to disable the remove button if this was the only paper selected in the session */
                        var selectedPapers = $(this).siblings('tr#paper').filter('.selected');
                        if (selectedPapers.length == 0) {
                            $(this).parents('table.paper-table').siblings('.session-deselector').addClass('disabled');
                        }
                    }
                }
                else {
                    /* if we are selecting a previously unselected paper */
                    addToChosen(exactStartingTime, paperObject, 'paper');
                    $(this).addClass('selected');

                    /* if we are not being triggered at the session level, then we need to handle the state of the session level button ourselves */
                    if (!fromSession) {

                        /* we also need to enable the remove button */
                        $(this).parents('table.paper-table').siblings('.session-deselector').removeClass('disabled');

                        /* and disable the choose button if all the papers are now selected anyway */
                        var sessionPapers = $(this).siblings('tr#paper');
                        var selectedPapers = sessionPapers.filter('.selected');
                        if (sessionPapers.length == selectedPapers.length) {
                            $(this).parents('table.paper-table').siblings('.session-selector').addClass('disabled');
                        }
                    }
                }
            });
        });
    </script>
---
<link rel="stylesheet" href="/assets/css/alertify.css" id="alertifyCSS">
<table id="hidden-program-table">
<thead>
<tr><th>time</th><th>location</th><th>info</th></tr></thead>
<tbody></tbody>
</table>
<div id="introParagraph">
<p>On this page, you can choose the sessions (and individual papers/posters) of your choice <em>and</em> generate a PDF of your customized schedule! This page should work on modern browsers on all operating systems. On mobile devices, Safari on iOS and Chrome on Android are the only browsers known to work. For the best experience, use a non-mobile device with a resolution of at least 1920x1080. For help, simply type "?"" while on the page or click on the "Help" button.</p>
</div>
<p class="text-center">
<a href="#" id="help-button" class="btn btn--small btn--twitter">Help</a>
</p>
<p class="text-center">
<a href="#" id="toggle-all-button" class="btn btn--small btn--twitter">Expand All Sessions ↓</a>
</p>
<div class="schedule">
<div class="day" id="day-1">Sunday, June 02, 2019</div>
<div class="session session-break session-plenary" id="session-break-1"><span class="session-title">Breakfast</span><br/><span class="session-time" title="Sunday, June 02, 2019">07:30 &ndash; 09:00</span></div>
<div class="session session-expandable session-tutorials"><div id="expander"></div><a href="#" class="session-title">Morning Tutorials</a><br/><span class="session-time" title="Sunday, June 02, 2019">9:00 &ndash; 12:30</span><br/><div class="tutorial-session-details"><br/><table class="tutorial-table">
<tr id="tutorial"><td><span class="tutorial-title"><strong>Deep Adversarial Learning for NLP. </strong>William Yang Wang, Sameer Singh and Jiwei Li. </span><br/><span class="btn btn--location inline-location">Greenway DE/FG</span></td></tr>
<tr id="tutorial"><td><span class="tutorial-title"><strong>Deep Learning for Natural Language Inference. </strong>Samuel Bowman and Xiaodan Zhu. </span><br/><span class="btn btn--location inline-location">Greenway BC/HI</span></td></tr>
<tr id="tutorial"><td><span class="tutorial-title"><strong>Measuring and Modeling Language Change. </strong> and Jacob Eisenstein. </span><br/><span class="btn btn--location inline-location">Greenway J</span></td></tr>
</table>
</div>
</div>
<div class="session session-break session-plenary" id="session-break-2"><span class="session-title">Morning Break</span><br/><span class="session-time" title="Sunday, June 02, 2019">10:30 &ndash; 11:00</span></div>
<div class="session session-break session-plenary" id="session-break-3"><span class="session-title">Lunch Break</span><br/><span class="session-time" title="Sunday, June 02, 2019">12:30 &ndash; 14:00</span></div>
<div class="session session-expandable session-tutorials"><div id="expander"></div><a href="#" class="session-title">Afternoon Tutorials</a><br/><span class="session-time" title="Sunday, June 02, 2019">14:00 &ndash; 17:30</span><br/><div class="tutorial-session-details"><br/><table class="tutorial-table">
<tr id="tutorial"><td><span class="tutorial-title"><strong>Transfer Learning in Natural Language Processing. </strong>Sebastian Ruder, Matthew E. Peters, Swabha Swayamdipta and Thomas Wolf. </span><br/><span class="btn btn--location inline-location">Greenway DE/FG</span></td></tr>
<tr id="tutorial"><td><span class="tutorial-title"><strong>Language Learning and Processing in People and Machines. </strong>Aida Nematzadeh, Richard Futrell and Roger Levy. </span><br/><span class="btn btn--location inline-location">Greenway BC/HI</span></td></tr>
<tr id="tutorial"><td><span class="tutorial-title"><strong>Applications of Natural Language Processing in Clinical Research and Practice. </strong>Yanshan Wang, Ahmad Tafti, Sunghwan Sohn and Rui Zhang. </span><br/><span class="btn btn--location inline-location">Greenway J</span></td></tr>
</table>
</div>
</div>
<div class="session session-break session-plenary" id="session-break-4"><span class="session-title">Afternoon Break</span><br/><span class="session-time" title="Sunday, June 02, 2019">15:30 &ndash; 16:00</span></div>
<div class="session session-plenary"><span class="session-title">Welcome Reception</span><br/><span class="session-time" title="Sunday, June 02, 2019">18:00 &ndash; 20:00</span><br/><span class="session-location btn btn--location">Nicollet Ballroom</span></div>
<div class="day" id="day-2">Monday, June 03, 2019</div>
<div class="session session-plenary"><span class="session-title">Land Acknowledgments, Opening Remarks and Janyce Weibe and Richard Kittredge Remembrances</span><br/><span class="session-time" title="Monday, June 03, 2019">9:00 &ndash; 9:30</span><br/><span class="session-location btn btn--location">Nicollet Grand Ballroom</span></div>
<div class="session session-expandable session-plenary"><div id="expander"></div><a href="#" class="session-title"><strong>Keynote 1: Arvind Narayanan "Data as a Mirror of Society: Lessons from the Emerging Science of Fairness in Machine Learning"</strong></a><br/><span class="session-person"><a href="http://randomwalker.info" target="_blank">Arvind Narayanan</a></span><br/><span class="session-time" title="Monday, June 03, 2019">9:30 &ndash; 10:30</span><br/><span class="session-location btn btn--location">Nicollet Grand Ballroom</span><div class="paper-session-details"><br/><div class="session-abstract"><p>Language corpora reflect human society, including cultural stereotypes, prejudices, and historical patterns. By default, statistical language models will absorb these stereotypes. As a result, NLP systems for word analogy generation, toxicity detection, and many other tasks have been found to reflect racial and gender biases. Based on this observation, I will discuss two emerging research directions. First, a deeper understanding of human culture can help identify possible harmful stereotypes in algorithmic systems. The second research direction is the converse of the first: if data is a mirror of society, machine learning can be used as a magnifying lens to study human culture.</p></div></div></div>
<div class="session session-break session-plenary" id="session-break-5"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Monday, June 03, 2019">10:30 &ndash; 11:00</span></div>
<div class="session-box" id="session-box-1">
<div class="session-header" id="session-header-1">Long Orals / Long & Short Posters</div>
<div class="session session-expandable session-papers1" id="session-1a"><div id="expander"></div><a href="#" class="session-title">1A: Cognitive</a><br/><span class="session-time" title="Monday, June 03, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-1a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-1a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Serguei Pakhomov</td></tr>
<tr id="paper" paper-id="179"><td id="paper-time">11:00&ndash;11:18</td><td><span class="paper-title">Entity Recognition at First Sight: Improving NER with Eye Movement Information. </span><em>Nora Hollenstein and Ce Zhang</em></td></tr>
<tr id="paper" paper-id="1465"><td id="paper-time">11:18&ndash;11:36</td><td><span class="paper-title">The emergence of number and syntax units in LSTM language models. </span><em>Yair Lakretz, Germán Kruszewski, Théo Desbordes, Dieuwke Hupkes, Stanislas Dehaene and Marco Baroni</em></td></tr>
<tr id="paper" paper-id="1495"><td id="paper-time">11:36&ndash;11:54</td><td><span class="paper-title">Neural Self-Training through Spaced Repetition. </span><em> and Hadi Amiri</em></td></tr>
<tr id="paper" paper-id="1768"><td id="paper-time">11:54&ndash;12:12</td><td><span class="paper-title">Neural language models as psycholinguistic subjects: Representations of syntactic state. </span><em>Richard Futrell, Ethan Wilcox, Takashi Morita, Peng Qian, Miguel Ballesteros and Roger Levy</em></td></tr>
<tr id="paper" paper-id="2241"><td id="paper-time">12:12&ndash;12:30</td><td><span class="paper-title">Understanding language-elicited EEG data by predicting it from a fine-tuned language model. </span><em>Dan Schwartz and Tom Mitchell</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers2" id="session-1b"><div id="expander"></div><a href="#" class="session-title">1B: Speech</a><br/><span class="session-time" title="Monday, June 03, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Nicollet A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-1b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-1b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Yang Liu</td></tr>
<tr id="paper" paper-id="202"><td id="paper-time">11:00&ndash;11:18</td><td><span class="paper-title">Pre-training on high-resource speech recognition improves low-resource speech-to-text translation. </span><em>Sameer Bansal, Herman Kamper, Karen Livescu, Adam Lopez and Sharon Goldwater</em></td></tr>
<tr id="paper" paper-id="1507"><td id="paper-time">11:18&ndash;11:36</td><td><span class="paper-title">Measuring the perceptual availability of phonological features during language acquisition using unsupervised binary stochastic autoencoders. </span><em>Cory Shain and Micha Elsner</em></td></tr>
<tr id="paper" paper-id="1870"><td id="paper-time">11:36&ndash;11:54</td><td><span class="paper-title">Giving Attention to the Unexpected: Using Prosody Innovations in Disfluency Detection. </span><em>Vicky Zayats and Mari Ostendorf</em></td></tr>
<tr id="paper" paper-id="1998"><td id="paper-time">11:54&ndash;12:12</td><td><span class="paper-title">Massively Multilingual Adversarial Speech Recognition. </span><em>Oliver Adams, Matthew Wiesner, Shinji Watanabe and David Yarowsky</em></td></tr>
<tr id="paper" paper-id="2189"><td id="paper-time">12:12&ndash;12:30</td><td><span class="paper-title">Lost in Interpretation: Predicting Untranslated Terminology in Simultaneous Interpretation. </span><em>Nikolai Vogler, Craig Stewart and Graham Neubig</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers3" id="session-1c"><div id="expander"></div><a href="#" class="session-title">1C: Generation</a><br/><span class="session-time" title="Monday, June 03, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Northstar A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-1c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-1c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Wei Xu</td></tr>
<tr id="paper" paper-id="132"><td id="paper-time">11:00&ndash;11:18</td><td><span class="paper-title">AudioCaps: Generating Captions for Audios in The Wild. </span><em>Chris Dongjoo Kim, Byeongchang Kim, Hyunmin Lee and Gunhee Kim</em></td></tr>
<tr id="paper" paper-id="1498"><td id="paper-time">11:18&ndash;11:36</td><td><span class="paper-title">“President Vows to Cut &lt;Taxes&gt; Hair”: Dataset and Analysis of Creative Text Editing for Humorous Headlines. </span><em>Nabil Hossain, John Krumm and Michael Gamon</em></td></tr>
<tr id="paper" paper-id="886"><td id="paper-time">11:36&ndash;11:54</td><td><span class="paper-title">Answer-based Adversarial Training for Generating Clarification Questions. </span><em>Sudha Rao and Hal Daumé III</em></td></tr>
<tr id="paper" paper-id="1182"><td id="paper-time">11:54&ndash;12:12</td><td><span class="paper-title">Improving Grammatical Error Correction via Pre-Training a Copy-Augmented Architecture with Unlabeled Data. </span><em>Wei Zhao, Liang Wang, Kewei Shen, Ruoyu Jia and Jingming Liu</em></td></tr>
<tr id="paper" paper-id="296"><td id="paper-time">12:12&ndash;12:30</td><td><span class="paper-title">Topic-Guided Variational Auto-Encoder for Text Generation. </span><em>Wenlin Wang, Zhe Gan, Hongteng Xu, Ruiyi Zhang, Guoyin Wang, Dinghan Shen, Changyou Chen and Lawrence Carin</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers4" id="session-1d"><div id="expander"></div><a href="#" class="session-title">1D: Syntax</a><br/><span class="session-time" title="Monday, June 03, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Greenway</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-1d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-1d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Roi Reichart</td></tr>
<tr id="paper" paper-id="333"><td id="paper-time">11:00&ndash;11:18</td><td><span class="paper-title">Implementation of a Chomsky-Schützenberger n-best parser for weighted multiple context-free grammars. </span><em>Thomas Ruprecht and Tobias Denkinger</em></td></tr>
<tr id="paper" paper-id="370"><td id="paper-time">11:18&ndash;11:36</td><td><span class="paper-title">Phylogenic Multi-Lingual Dependency Parsing. </span><em>Mathieu Dehouck and Pascal Denis</em></td></tr>
<tr id="paper" paper-id="699"><td id="paper-time">11:36&ndash;11:54</td><td><span class="paper-title">Discontinuous Constituency Parsing with a Stack-Free Transition System and a Dynamic Oracle. </span><em>Maximin Coavoux and Shay B. Cohen</em></td></tr>
<tr id="paper" paper-id="1005"><td id="paper-time">11:54&ndash;12:12</td><td><span class="paper-title">How Bad are PoS Tagger in Cross-Corpora Settings? Evaluating Annotation Divergence in the UD Project.. </span><em>Guillaume Wisniewski and François Yvon</em></td></tr>
<tr id="paper" paper-id="2066"><td id="paper-time">12:12&ndash;12:30</td><td><span class="paper-title">CCG Parsing Algorithm with Incremental Tree Rotation. </span><em>Miloš Stanojević and Mark Steedman</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers5" id="session-1e"><div id="expander"></div><a href="#" class="session-title">1E: Theory</a><br/><span class="session-time" title="Monday, June 03, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Nicollet D</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-1e-selector"> Choose All</a><a href="#" class="session-deselector" id="session-1e-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Ryan Cotterell</td></tr>
<tr id="paper" paper-id="1478"><td id="paper-time">11:00&ndash;11:18</td><td><span class="paper-title">Cyclical Annealing Schedule: A Simple Approach to Mitigating KL Vanishing. </span><em>Hao Fu, Chunyuan Li, Xiaodong Liu, Jianfeng Gao, Asli Celikyilmaz and Lawrence Carin</em></td></tr>
<tr id="paper" paper-id="1683"><td id="paper-time">11:18&ndash;11:36</td><td><span class="paper-title">Recurrent models and lower bounds for projective syntactic decoding. </span><em> and Natalie Schluter</em></td></tr>
<tr id="paper" paper-id="1730"><td id="paper-time">11:36&ndash;11:54</td><td><span class="paper-title">Evaluating Composition Models for Verb Phrase Elliptical Sentence Embeddings. </span><em>Gijs Wijnholds and Mehrnoosh Sadrzadeh</em></td></tr>
<tr id="paper" paper-id="1791"><td id="paper-time">11:54&ndash;12:12</td><td><span class="paper-title">Neural Finite-State Transducers: Beyond Rational Relations. </span><em>Chu-Cheng Lin, Hao Zhu, Matthew R. Gormley and Jason Eisner</em></td></tr>
<tr id="paper" paper-id="2151"><td id="paper-time">12:12&ndash;12:30</td><td><span class="paper-title">Riemannian Normalizing Flow on Variational Wasserstein Autoencoder for Text Modeling. </span><em>Prince Zizhuang Wang and William Yang Wang</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-posters" id="session-poster-1"><div id="expander"></div><a href="#" class="session-title">1F: Question Answering, Sentiment, Machine Translation, Resources & Evaluation (Posters) </a><br/><span class="session-time" title="Monday, June 03, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Hyatt Exhibit Hall</span><div class="poster-session-details"><br/><table class="poster-table">
<tr><td><span class="poster-type">Question Answering</span></td></tr>
<tr id="poster" poster-id="584"><td><span class="poster-title">A Study of Incorrect Paraphrases in Crowdsourced User Utterances. </span><em>Mohammad-Ali Yaghoub-Zadeh-Fard, Boualem Benatallah, Moshe Chai Barukh and Shayan Zamanirad</em></td></tr>
<tr id="poster" poster-id="633"><td><span class="poster-title">ComQA: A Community-sourced Dataset for Complex Factoid Question Answering with Paraphrase Clusters. </span><em>Abdalghani Abujabal, Rishiraj Saha Roy, Mohamed Yahya and Gerhard Weikum</em></td></tr>
<tr id="poster" poster-id="696"><td><span class="poster-title">FreebaseQA: A New Factoid QA Data Set Matching Trivia-Style Question-Answer Pairs with Freebase. </span><em>Kelvin Jiang, Dekun Wu and Hui Jiang</em></td></tr>
<tr id="poster" poster-id="758"><td><span class="poster-title">Simple Question Answering with Subgraph Ranking and Joint-Scoring. </span><em>Wenbo Zhao, Tagyoung Chung, Anuj Goyal and Angeliki Metallinou</em></td></tr>
<tr id="poster" poster-id="829"><td><span class="poster-title">Learning to Attend On Essential Terms: An Enhanced Retriever-Reader Model for Open-domain Question Answering. </span><em>Jianmo Ni, Chenguang Zhu, Weizhu Chen and Julian McAuley</em></td></tr>
<tr id="poster" poster-id="846"><td><span class="poster-title">UHop: An Unrestricted-Hop Relation Extraction Framework for Knowledge-Based Question Answering. </span><em>Zi-Yuan Chen, Chih-Hung Chang, Yi-Pei Chen, Jijnasa Nayak and Lun-Wei Ku</em></td></tr>
<tr id="poster" poster-id="995"><td><span class="poster-title">BAG: Bi-directional Attention Entity Graph Convolutional Network for Multi-hop Reasoning Question Answering. </span><em>Yu Cao, Meng Fang and Dacheng Tao</em></td></tr>
<tr id="poster" poster-id="54-srw"><td><span class="poster-title">Is It Dish Washer Safe? Automatically Answering “Yes/No” Questions Using Customer Reviews. </span><em>Daria Dzendzik, Carl Vogel and Jennifer Foster</em></td></tr>
<tr><td><span class="poster-type">Sentiment</span></td></tr>
<tr id="poster" poster-id="173"><td><span class="poster-title">Vector of Locally-Aggregated Word Embeddings (VLAWE): A Novel Document-level Representation. </span><em>Radu Tudor Ionescu and Andrei Butnaru</em></td></tr>
<tr id="poster" poster-id="221"><td><span class="poster-title">Multi-task Learning for Multi-modal Emotion Recognition and Sentiment Analysis. </span><em>Md Shad Akhtar, Dushyant Chauhan, Deepanway Ghosal, Soujanya Poria, Asif Ekbal and Pushpak Bhattacharyya</em></td></tr>
<tr id="poster" poster-id="455"><td><span class="poster-title">Utilizing BERT for Aspect-Based Sentiment Analysis via Constructing Auxiliary Sentence. </span><em>Chi Sun, Luyao Huang and Xipeng Qiu</em></td></tr>
<tr id="poster" poster-id="641"><td><span class="poster-title">A Variational Approach to Weakly Supervised Document-Level Multi-Aspect Sentiment Classification. </span><em>Ziqian Zeng, Wenxuan Zhou, Xin Liu and Yangqiu Song</em></td></tr>
<tr id="poster" poster-id="1093"><td><span class="poster-title">HiGRU: Hierarchical Gated Recurrent Units for Utterance-Level Emotion Recognition. </span><em>Wenxiang Jiao, Haiqin Yang, Irwin King and Michael R. Lyu</em></td></tr>
<tr id="poster" poster-id="1460"><td><span class="poster-title">Learning Interpretable Negation Rules via Weak Supervision at Document Level: A Reinforcement Learning Approach. </span><em>Nicolas Pröllochs, Stefan Feuerriegel and Dirk Neumann</em></td></tr>
<tr id="poster" poster-id="2023"><td><span class="poster-title">Simplified Neural Unsupervised Domain Adaptation. </span><em> and Timothy Miller</em></td></tr>
<tr id="poster" poster-id="2261"><td><span class="poster-title">Learning Bilingual Sentiment-Specific Word Embeddings without Cross-lingual Supervision. </span><em>Yanlin Feng and Xiaojun Wan</em></td></tr>
<tr><td><span class="poster-type">Machine Translation</span></td></tr>
<tr id="poster" poster-id="514"><td><span class="poster-title">ReWE: Regressing Word Embeddings for Regularization of Neural Machine Translation Systems. </span><em>Inigo Jauregi Unanue, Ehsan Zare Borzeshi, Nazanin Esmaili and Massimo Piccardi</em></td></tr>
<tr id="poster" poster-id="782"><td><span class="poster-title">Lost in Machine Translation: A Method to Reduce Meaning Loss. </span><em>Reuben Cohn-Gordon and Noah Goodman</em></td></tr>
<tr id="poster" poster-id="830"><td><span class="poster-title">Bi-Directional Differentiable Input Reconstruction for Low-Resource Neural Machine Translation. </span><em>Xing Niu, Weijia Xu and Marine Carpuat</em></td></tr>
<tr id="poster" poster-id="839"><td><span class="poster-title">Code-Switching for Enhancing NMT with Pre-Specified Translation. </span><em>Kai Song, Yue Zhang, Heng Yu, Weihua Luo, Kun Wang and Min Zhang</em></td></tr>
<tr id="poster" poster-id="894"><td><span class="poster-title">Aligning Vector-spaces with Noisy Supervised Lexicon. </span><em>Noa Yehezkel Lubin, Jacob Goldberger and Yoav Goldberg</em></td></tr>
<tr id="poster" poster-id="1019"><td><span class="poster-title">Understanding and Improving Hidden Representations for Neural Machine Translation. </span><em>Guanlin Li, Lemao Liu, Xintong Li, Conghui Zhu, Tiejun Zhao and Shuming Shi</em></td></tr>
<tr><td><span class="poster-type">Resources and Evaluation</span></td></tr>
<tr id="poster" poster-id="287"><td><span class="poster-title">Content Differences in Syntactic and Semantic Representation. </span><em>Daniel Hershcovich, Omri Abend and Ari Rappoport</em></td></tr>
<tr id="poster" poster-id="747"><td><span class="poster-title">Attentive Mimicking: Better Word Embeddings by Attending to Informative Contexts. </span><em>Timo Schick and Hinrich Schütze</em></td></tr>
<tr id="poster" poster-id="813"><td><span class="poster-title">Evaluating Style Transfer for Text. </span><em>Remi Mir, Bjarke Felbo, Nick Obradovich and Iyad Rahwan</em></td></tr>
<tr id="poster" poster-id="1310"><td><span class="poster-title">Big BiRD: A Large, Fine-Grained, Bigram Relatedness Dataset for Examining Semantic Composition. </span><em>Shima Asaadi, Saif Mohammad and Svetlana Kiritchenko</em></td></tr>
<tr id="poster" poster-id="1541"><td><span class="poster-title">Outlier Detection for Improved Data Quality and Diversity in Dialog Systems. </span><em>Stefan Larson, Anish Mahendran, Andrew Lee, Jonathan K. Kummerfeld, Parker Hill, Michael A. Laurenzano, Johann Hauswald, Lingjia Tang and Jason Mars</em></td></tr>
<tr id="poster" poster-id="1771"><td><span class="poster-title">Asking the Right Question: Inferring Advice-Seeking Intentions from Personal Narratives. </span><em>Liye Fu, Jonathan P. Chang and Cristian Danescu-Niculescu-Mizil</em></td></tr>
<tr id="poster" poster-id="1896"><td><span class="poster-title">Seeing Things from a Different Angle:Discovering Diverse Perspectives about Claims. </span><em>Sihao Chen, Daniel Khashabi, Wenpeng Yin, Chris Callison-Burch and Dan Roth</em></td></tr>
</table>
</div>
</div>
</div>
<div class="session session-break session-plenary" id="session-break-6"><span class="session-title">Grab your lunch break</span><br/><span class="session-time" title="Monday, June 03, 2019">12:30 &ndash; 13:00</span></div>
<div class="session session-expandable session-plenary"><div id="expander"></div><a href="#" class="session-title"><strong>Careers in NLP Panel</strong></a><br/><span class="session-time" title="Monday, June 03, 2019">13:00 &ndash; 14:30</span><br/><span class="session-location btn btn--location">Nicollet Grand Ballroom</span><div class="paper-session-details"><br/><div class="session-abstract"><p>The 2019 version of this panel recognizes the diversity of NLP careers today. Traditional career paths have typically led NLP researchers into academia, industrial labs, and government agencies. Today, we also see an increase in roles at startup companies and an emerging NLP practitioner role in industry that intersects with software, data, and product. The panel will discuss multiple topics including trends in NLP careers, emerging skills, prominent challenges and opportunities for cross-functional collaboration as an NLP professional in today's organizations. Panelists include Judith L. Klavans (Independent), Yunyao Li (IBM Research), Owen Rambow (Elemental Cognition), Joel Tetreault (Grammarly). Moderated by Philip Resnik (University of Maryland).</p></div></div></div>
<div class="session session-break session-plenary" id="session-break-7"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Monday, June 03, 2019">14:30 &ndash; 15:00</span></div>
<div class="session-box" id="session-box-2">
<div class="session-header" id="session-header-2">Short Orals / Long & Short Posters / Demos</div>
<div class="session session-expandable session-papers1" id="session-2a"><div id="expander"></div><a href="#" class="session-title">2A: Dialogue & Discourse</a><br/><span class="session-time" title="Monday, June 03, 2019">15:00 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Northstar A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-2a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-2a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Ellen Riloff</td></tr>
<tr id="paper" paper-id="1589"><td id="paper-time">15:00&ndash;15:15</td><td><span class="paper-title">IMHO Fine-Tuning Improves Claim Detection. </span><em>Tuhin Chakrabarty, Christopher Hidey and Kathy McKeown</em></td></tr>
<tr id="paper" paper-id="1658"><td id="paper-time">15:15&ndash;15:30</td><td><span class="paper-title">Joint Multiple Intent Detection and Slot Labeling for Goal-Oriented Dialog. </span><em>Rashmi Gangadharaiah and Balakrishnan Narayanaswamy</em></td></tr>
<tr id="paper" paper-id="1734"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">CITE: A Corpus of Image-Text Discourse Relations. </span><em>Malihe Alikhani, Sreyasi Nag Chowdhury, Gerard de Melo and Matthew Stone</em></td></tr>
<tr id="paper" paper-id="1936"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">Improving Dialogue State Tracking by Discerning the Relevant Context. </span><em>Sanuj Sharma, Prafulla Kumar Choubey and Ruihong Huang</em></td></tr>
<tr id="paper" paper-id="2085"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">CLEVR-Dialog: A Diagnostic Dataset for Multi-Round Reasoning in Visual Dialog. </span><em>Satwik Kottur, José M. F. Moura, Devi Parikh, Dhruv Batra and Marcus Rohrbach</em></td></tr>
<tr id="paper" paper-id="2308"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">Learning Outside the Box: Discourse-level Features Improve Metaphor Identification. </span><em>Jesse Mu, Helen Yannakoudakis and Ekaterina Shutova</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers2" id="session-2b"><div id="expander"></div><a href="#" class="session-title">2B: Ethics, Bias & Fairness</a><br/><span class="session-time" title="Monday, June 03, 2019">15:00 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-2b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-2b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Preslav Nakov</td></tr>
<tr id="paper" paper-id="640"><td id="paper-time">15:00&ndash;15:15</td><td><span class="paper-title">Detection of Abusive Language: the Problem of Biased Datasets. </span><em>Michael Wiegand, Josef Ruppenhofer and Thomas Kleinbauer</em></td></tr>
<tr id="paper" paper-id="1172"><td id="paper-time">15:15&ndash;15:30</td><td><span class="paper-title">Lipstick on a Pig: Debiasing Methods Cover up Systematic Gender Biases in Word Embeddings But do not Remove Them. </span><em>Hila Gonen and Yoav Goldberg</em></td></tr>
<tr id="paper" paper-id="1450"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">Black is to Criminal as Caucasian is to Police: Detecting and Removing Multiclass Bias in Word Embeddings. </span><em>Thomas Manzini, Lim Yao Chong, Alan W. Black and Yulia Tsvetkov</em></td></tr>
<tr id="paper" paper-id="2098"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">On Measuring Social Biases in Sentence Encoders. </span><em>Chandler May, Alex Wang, Shikha Bordia, Samuel R. Bowman and Rachel Rudinger</em></td></tr>
<tr id="paper" paper-id="2117"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">Gender Bias in Contextualized Word Embeddings. </span><em>Jieyu Zhao, Tianlu Wang, Mark Yatskar, Ryan Cotterell, Vicente Ordonez and Kai-Wei Chang</em></td></tr>
<tr id="paper" paper-id="65-srw"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">Identifying and Reducing Gender Bias in Word-Level Language Models. </span><em>Shikha Bordia and Samuel R. Bowman</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers3" id="session-2c"><div id="expander"></div><a href="#" class="session-title">2C: Style & Sentiment</a><br/><span class="session-time" title="Monday, June 03, 2019">15:00 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Nicollet D</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-2c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-2c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Diyi Yang</td></tr>
<tr id="paper" paper-id="1490"><td id="paper-time">15:00&ndash;15:15</td><td><span class="paper-title">Combining Sentiment Lexica with a Multi-View Variational Autoencoder. </span><em>Alexander Miserlis Hoyle, Lawrence Wolf-Sonkin, Hanna Wallach, Ryan Cotterell and Isabelle Augenstein</em></td></tr>
<tr id="paper" paper-id="178"><td id="paper-time">15:15&ndash;15:30</td><td><span class="paper-title">Enhancing Opinion Role Labeling with Semantic-Aware Word Representations from Semantic Role Labeling. </span><em>Meishan Zhang, Peili Liang and Guohong Fu</em></td></tr>
<tr id="paper" paper-id="1358"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">Frowning Frodo, Wincing Leia, and a Seriously Great Friendship: Learning to Classify Emotional Relationships of Fictional Characters. </span><em>Evgeny Kim and Roman Klinger</em></td></tr>
<tr id="paper" paper-id="1404"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">Generalizing Unmasking for Short Texts. </span><em>Janek Bevendorff, Benno Stein, Matthias Hagen and Martin Potthast</em></td></tr>
<tr id="paper" paper-id="334"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">Adversarial Training for Satire Detection: Controlling for Confounding Variables. </span><em>Robert McHardy, Heike Adel and Roman Klinger</em></td></tr>
<tr id="paper" paper-id="22-srw"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">Emotion Impacts Speech Recognition Performance. </span><em>Rushab Munot and Ani Nenkova</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers4" id="session-2d"><div id="expander"></div><a href="#" class="session-title">2D: Summarization & IR</a><br/><span class="session-time" title="Monday, June 03, 2019">15:00 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Nicollet A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-2d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-2d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Michael J. Paul</td></tr>
<tr id="paper" paper-id="790"><td id="paper-time">15:00&ndash;15:15</td><td><span class="paper-title">Keyphrase Generation: A Text Summarization Struggle. </span><em>Erion Çano and Ondřej Bojar</em></td></tr>
<tr id="paper" paper-id="1346"><td id="paper-time">15:15&ndash;15:30</td><td><span class="paper-title">SEQˆ3: Differentiable Sequence-to-Sequence-to-Sequence Autoencoder for Unsupervised Abstractive Sentence Compression. </span><em>Christos Baziotis, Ion Androutsopoulos, Ioannis Konstas and Alexandros Potamianos</em></td></tr>
<tr id="paper" paper-id="1638"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">Crowdsourcing Lightweight Pyramids for Manual Summary Evaluation. </span><em>Ori Shapira, David Gabay, Yang Gao, Hadar Ronen, Ramakanth Pasunuru, Mohit Bansal, Yael Amsterdamer and Ido Dagan</em></td></tr>
<tr id="paper" paper-id="1820"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">Serial Recall Effects in Neural Language Modeling. </span><em>Hassan Hajipoor, Hadi Amiri, Maseud Rahgozar and Farhad Oroumchian</em></td></tr>
<tr id="paper" paper-id="2310"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">Fast Concept Mention Grouping for Concept Map-based Multi-Document Summarization. </span><em>Tobias Falke and Iryna Gurevych</em></td></tr>
<tr id="paper" paper-id="14-srw"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">The Strength of the Weakest Supervision: Topic Classification Using Class Labels. </span><em>Jiatong Li, Kai Zheng, Hua Xu, Qiaozhu Mei and Yue Wang</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers5" id="session-2e"><div id="expander"></div><a href="#" class="session-title">2E: Syntax</a><br/><span class="session-time" title="Monday, June 03, 2019">15:00 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Greenway</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-2e-selector"> Choose All</a><a href="#" class="session-deselector" id="session-2e-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Joel Tetreault</td></tr>
<tr id="paper" paper-id="110"><td id="paper-time">15:00&ndash;15:15</td><td><span class="paper-title">Syntax-aware Neural Semantic Role Labeling with Supertags. </span><em>Jungo Kasai, Dan Friedman, Robert Frank, Dragomir Radev and Owen Rambow</em></td></tr>
<tr id="paper" paper-id="704"><td id="paper-time">15:15&ndash;15:30</td><td><span class="paper-title">Left-to-Right Dependency Parsing with Pointer Networks. </span><em>Daniel Fernández-González and Carlos Gómez-Rodríguez</em></td></tr>
<tr id="paper" paper-id="1081"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">Viable Dependency Parsing as Sequence Labeling. </span><em>Michalina Strzyz, David Vilares and Carlos Gómez-Rodríguez</em></td></tr>
<tr id="paper" paper-id="1754"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">Pooled Contextualized Embeddings for Named Entity Recognition. </span><em>Alan Akbik, Tanja Bergmann and Roland Vollgraf</em></td></tr>
<tr id="paper" paper-id="1969"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">Better Modeling of Incomplete Annotations for Named Entity Recognition. </span><em>Zhanming Jie, Pengjun Xie, Wei Lu, Ruixue Ding and Linlin Li</em></td></tr>
<tr id="paper" paper-id="44-srw"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">Handling Noisy Labels for Robustly Learning from Self-Training Data for Low-Resource Sequence Labeling. </span><em>Debjit Paul, Mittul Singh, Michael A. Hedderich and Dietrich Klakow</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-posters" id="session-poster-2"><div id="expander"></div><a href="#" class="session-title">2F: Information Extraction, Generation  & Semantics (Posters & Demos) </a><br/><span class="session-time" title="Monday, June 03, 2019">15:00 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Hyatt Exhibit Hall</span><div class="poster-session-details"><br/><table class="poster-table">
<tr><td><span class="poster-type">Information Extraction</span></td></tr>
<tr id="poster" poster-id="126"><td><span class="poster-title">Event Detection without Triggers. </span><em>Shulin Liu, Yang Li, Feng Zhang, Tao Yang and Xinpeng Zhou</em></td></tr>
<tr id="poster" poster-id="367"><td><span class="poster-title">Sub-event detection from twitter streams as a sequence labeling problem. </span><em>Giannis Bekoulis, Johannes Deleu, Thomas Demeester and Chris Develder</em></td></tr>
<tr id="poster" poster-id="569"><td><span class="poster-title">GraphIE: A Graph-Based Framework for Information Extraction. </span><em>Yujie Qian, Enrico Santus, Zhijing Jin, Jiang Guo and Regina Barzilay</em></td></tr>
<tr id="poster" poster-id="1718"><td><span class="poster-title">OpenKI: Integrating Open Information Extraction and Knowledge Bases with Relation Inference. </span><em>Dongxu Zhang, Subhabrata Mukherjee, Colin Lockard, Luna Dong and Andrew McCallum</em></td></tr>
<tr id="poster" poster-id="2074"><td><span class="poster-title">Imposing Label-Relational Inductive Bias for Extremely Fine-Grained Entity Typing. </span><em>Wenhan Xiong, Jiawei Wu, Deren Lei, Mo Yu, Shiyu Chang, Xiaoxiao Guo and William Yang Wang</em></td></tr>
<tr id="poster" poster-id="2076"><td><span class="poster-title">Improving Event Coreference Resolution by Learning Argument Compatibility from Unlabeled Data. </span><em>Yin Jou Huang, Jing Lu, Sadao Kurohashi and Vincent Ng</em></td></tr>
<tr id="poster" poster-id="2294"><td><span class="poster-title">Sentence Embedding Alignment for Lifelong Relation Extraction. </span><em>Hong Wang, Wenhan Xiong, Mo Yu, Xiaoxiao Guo, Shiyu Chang and William Yang Wang</em></td></tr>
<tr id="poster" poster-id="2335"><td><span class="poster-title">Description-Based Zero-shot Fine-Grained Entity Typing. </span><em>Rasha Obeidat, Xiaoli Fern, Hamed Shahbazi and Prasad Tadepalli</em></td></tr>
<tr id="poster" poster-id="30-srw"><td><span class="poster-title">Opinion Mining with Deep Contextualized Embeddings. </span><em>Wen-Bin Han and Noriko Kando</em></td></tr>
<tr id="poster" poster-id="4-srw"><td><span class="poster-title">A Bag-of-concepts Model Improves Relation Extraction in a Narrow Knowledge Domain with Limited Data. </span><em>Jiyu Chen, Karin Verspoor and Zenan Zhai</em></td></tr>
<tr><td><span class="poster-type">Generation</span></td></tr>
<tr id="poster" poster-id="2052"><td><span class="poster-title">Adversarial Decomposition of Text Representation. </span><em>Alexey Romanov, Anna Rumshisky, Anna Rogers and David Donahue</em></td></tr>
<tr id="poster" poster-id="2119"><td><span class="poster-title">PoMo: Generating Entity-Specific Post-Modifiers in Context. </span><em>Jun Seok Kang, Robert Logan, Zewei Chu, Yang Chen, Dheeru Dua, Kevin Gimpel, Sameer Singh and Niranjan Balasubramanian</em></td></tr>
<tr id="poster" poster-id="2184"><td><span class="poster-title">Improved Lexically Constrained Decoding for Translation and Monolingual Rewriting. </span><em>J. Edward Hu, Huda Khayrallah, Ryan Culkin, Patrick Xia, Tongfei Chen, Matt Post and Benjamin Van Durme</em></td></tr>
<tr id="poster" poster-id="2291"><td><span class="poster-title">Courteously Yours: Inducing courteous behavior in Customer Care responses using Reinforced Pointer Generator Network. </span><em>Hitesh Golchha, Mauajama Firdaus, Asif Ekbal and Pushpak Bhattacharyya</em></td></tr>
<tr id="poster" poster-id="2358"><td><span class="poster-title">How to Avoid Sentences Spelling Boring? Towards a Neural Approach to Unsupervised Metaphor Generation. </span><em>Zhiwei Yu and Xiaojun Wan</em></td></tr>
<tr id="poster" poster-id="19-srw"><td><span class="poster-title">Generating Text through Adversarial Training Using Skip-Thought Vectors. </span><em> and Afroz Ahamad</em></td></tr>
<tr id="poster" poster-id="38-srw"><td><span class="poster-title">A Partially Rule-Based Approach to AMR Generation. </span><em> and Emma Manning</em></td></tr>
<tr><td><span class="poster-type">Semantics</span></td></tr>
<tr id="poster" poster-id="526"><td><span class="poster-title">Incorporating Context and External Knowledge for Pronoun Coreference Resolution. </span><em>Hongming Zhang, Yan Song and Yangqiu Song</em></td></tr>
<tr id="poster" poster-id="642"><td><span class="poster-title">Unsupervised Deep Structured Semantic Models for Commonsense Reasoning. </span><em>Shuohang Wang, Sheng Zhang, Yelong Shen, Xiaodong Liu, Jingjing Liu, Jianfeng Gao and Jing Jiang</em></td></tr>
<tr id="poster" poster-id="1128"><td><span class="poster-title">Recovering dropped pronouns in Chinese conversations via modeling their referents. </span><em>Jingxuan Yang, Jianzhuo Tong, Si Li, Sheng Gao, Jun Guo and Nianwen Xue</em></td></tr>
<tr id="poster" poster-id="1203"><td><span class="poster-title">The problem with probabilistic DAG automata for semantic graphs. </span><em>Ieva Vasiljeva, Sorcha Gilroy and Adam Lopez</em></td></tr>
<tr id="poster" poster-id="1263"><td><span class="poster-title">A Systematic Study of Leveraging Subword Information for Learning Word Representations. </span><em>Yi Zhu, Ivan Vulić and Anna Korhonen</em></td></tr>
<tr id="poster" poster-id="1462"><td><span class="poster-title">Better Word Embeddings by Disentangling Contextual n-Gram Information. </span><em>Prakhar Gupta, Matteo Pagliardini and Martin Jaggi</em></td></tr>
<tr id="poster" poster-id="1492"><td><span class="poster-title">Integration of Knowledge Graph Embedding Into Topic Modeling with Hierarchical Dirichlet Process. </span><em>Dingcheng Li, Siamak Zamani, Jingyuan Zhang and Ping Li</em></td></tr>
<tr id="poster" poster-id="1721"><td><span class="poster-title">Correlation Coefficients and Semantic Textual Similarity. </span><em>Vitalii Zhelezniak, Aleksandar Savkov, April Shen and Nils Hammerla</em></td></tr>
<tr id="poster" poster-id="2387"><td><span class="poster-title">Generating Token-Level Explanations for Natural Language Inference. </span><em>James Thorne, Andreas Vlachos, Christos Christodoulopoulos and Arpit Mittal</em></td></tr>
<tr id="poster" poster-id="2424"><td><span class="poster-title">Strong Baselines for Complex Word Identification across Multiple Languages. </span><em>Pierre Finnimore, Elisabeth Fritzsch, Daniel King, Alison Sneyd, Aneeq Ur Rehman, Fernando Alva-Manchego and Andreas Vlachos</em></td></tr>
<tr id="poster" poster-id="58-srw"><td><span class="poster-title">Computational Investigations of Pragmatic Effects in Natural Language. </span><em> and Jad Kabbara</em></td></tr>
<tr id="poster" poster-id="30-demos"><td><span class="poster-title">Abbreviation Explorer - an interactive system for pre-evaluation of Unsupervised Abbreviation Disambiguation. </span><em>Manuel Ciosici and Ira Assent</em></td></tr>
<tr id="poster" poster-id="17-demos"><td><span class="poster-title">ADIDA: Automatic Dialect Identification for Arabic. </span><em>Ossama Obeid, Mohammad Salameh, Houda Bouamor and Nizar Habash</em></td></tr>
<tr id="poster" poster-id="47-demos"><td><span class="poster-title">Enabling Search and Collaborative Assembly of Causal Interactions Extracted from Multilingual and Multi-domain Free Text. </span><em>George C. G. Barbosa, Zechy Wong, Gus Hahn-Powell, Dane Bell, Rebecca Sharp, Marco A. Valenzuela-Escárcega and Mihai Surdeanu</em></td></tr>
<tr id="poster" poster-id="1-demos"><td><span class="poster-title">INS: An Interactive Chinese News Synthesis System. </span><em>Hui Liu, Wentao Qin and Xiaojun Wan</em></td></tr>
<tr id="poster" poster-id="59-demos"><td><span class="poster-title">Learning to Respond to Mixed-code Queries using Bilingual Word Embeddings. </span><em>Chia-Fang Ho, Jason Chang, Jhih-Jie Chen and Chingyu Yang</em></td></tr>
<tr id="poster" poster-id="18-demos"><td><span class="poster-title">Train, Sort, Explain: Learning to Diagnose Translation Models. </span><em>Robert Schwarzenberg, David Harbecke, Vivien Macketanz, Eleftherios Avramidis and Sebastian Möller</em></td></tr>
</table>
</div>
</div>
</div>
<div class="session session-break session-plenary" id="session-break-8"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Monday, June 03, 2019">16:30 &ndash; 17:00</span></div>
<div class="session-box" id="session-box-3">
<div class="session-header" id="session-header-3">Long Orals / Long & Short Posters / Demos</div>
<div class="session session-expandable session-papers1" id="session-3a"><div id="expander"></div><a href="#" class="session-title">3A: IE & IR</a><br/><span class="session-time" title="Monday, June 03, 2019">17:00 &ndash; 18:30</span><br/><span class="session-location btn btn--location">Nicollet A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-3a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-3a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Gerard de Melo</td></tr>
<tr id="paper" paper-id="676"><td id="paper-time">17:00&ndash;17:18</td><td><span class="paper-title">Adaptive Convolution for Multi-Relational Learning. </span><em>Xiaotian Jiang, Quan Wang and Bin Wang</em></td></tr>
<tr id="paper" paper-id="961"><td id="paper-time">17:18&ndash;17:36</td><td><span class="paper-title">Graph Pattern Entity Ranking Model for Knowledge Graph Completion. </span><em>Takuma Ebisu and Ryutaro Ichise</em></td></tr>
<tr id="paper" paper-id="1282"><td id="paper-time">17:36&ndash;17:54</td><td><span class="paper-title">Adversarial Training for Weakly Supervised Event Detection. </span><em>Xiaozhi Wang, Xu Han, Zhiyuan Liu, Maosong Sun and Peng Li</em></td></tr>
<tr id="paper" paper-id="2273"><td id="paper-time">17:54&ndash;18:12</td><td><span class="paper-title">A Submodular Feature-Aware Framework for Label Subset Selection in Extreme Classification Problems. </span><em>Elham J. Barezi, Ian D. Wood, Pascale Fung and Hamid R. Rabiee</em></td></tr>
<tr id="paper" paper-id="2372"><td id="paper-time">18:12&ndash;18:30</td><td><span class="paper-title">Relation Extraction with Temporal Reasoning Based on Memory Augmented Distant Supervision. </span><em>Jianhao Yan, Lin He, Ruqin Huang, Jian Li and Ying Liu</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers2" id="session-3b"><div id="expander"></div><a href="#" class="session-title">3B: Semantics</a><br/><span class="session-time" title="Monday, June 03, 2019">17:00 &ndash; 18:30</span><br/><span class="session-location btn btn--location">Nicollet D</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-3b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-3b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Kevin Gimpel</td></tr>
<tr id="paper" paper-id="181"><td id="paper-time">17:00&ndash;17:18</td><td><span class="paper-title">Integrating Semantic Knowledge to Tackle Zero-shot Text Classification. </span><em>Jingqing Zhang, Piyawat Lertvittayakumjorn and Yike Guo</em></td></tr>
<tr id="paper" paper-id="787"><td id="paper-time">17:18&ndash;17:36</td><td><span class="paper-title">Word-Node2Vec: Improving Word Embedding with Document-Level Non-Local Word Co-occurrences. </span><em>Procheta Sen, Debasis Ganguly and Gareth Jones</em></td></tr>
<tr id="paper" paper-id="1579"><td id="paper-time">17:36&ndash;17:54</td><td><span class="paper-title">Cross-Topic Distributional Semantic Representations Via Unsupervised Mappings. </span><em>Eleftheria Briakou, Nikos Athanasiou and Alexandros Potamianos</em></td></tr>
<tr id="paper" paper-id="1868"><td id="paper-time">17:54&ndash;18:12</td><td><span class="paper-title">What just happened? Evaluating retrofitted distributional word vectors. </span><em> and Dmetri Hayes</em></td></tr>
<tr id="paper" paper-id="2049"><td id="paper-time">18:12&ndash;18:30</td><td><span class="paper-title">Linguistic Knowledge and Transferability of Contextual Representations. </span><em>Nelson F. Liu, Matt Gardner, Yonatan Belinkov, Matthew E. Peters and Noah A. Smith</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers3" id="session-3c"><div id="expander"></div><a href="#" class="session-title">3C: Parsing</a><br/><span class="session-time" title="Monday, June 03, 2019">17:00 &ndash; 18:30</span><br/><span class="session-location btn btn--location">Greenway</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-3c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-3c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Kai-Wei Chang</td></tr>
<tr id="paper" paper-id="239"><td id="paper-time">17:00&ndash;17:18</td><td><span class="paper-title">Mutual Information Maximization for Simple and Accurate Part-Of-Speech Induction. </span><em> and Karl Stratos</em></td></tr>
<tr id="paper" paper-id="503"><td id="paper-time">17:18&ndash;17:36</td><td><span class="paper-title">Unsupervised Recurrent Neural Network Grammars. </span><em>Yoon Kim, Alexander Rush, Lei Yu, Adhiguna Kuncoro, Chris Dyer and Gábor Melis</em></td></tr>
<tr id="paper" paper-id="729"><td id="paper-time">17:36&ndash;17:54</td><td><span class="paper-title">Cooperative Learning of Disjoint Syntax and Semantics. </span><em>Serhii Havrylov, Germán Kruszewski and Armand Joulin</em></td></tr>
<tr id="paper" paper-id="862"><td id="paper-time">17:54&ndash;18:12</td><td><span class="paper-title">Unsupervised Latent Tree Induction with Deep Inside-Outside Recursive Auto-Encoders. </span><em>Andrew Drozdov, Patrick Verga, Mohit Yadav, Mohit Iyyer and Andrew McCallum</em></td></tr>
<tr id="paper" paper-id="1623"><td id="paper-time">18:12&ndash;18:30</td><td><span class="paper-title">Knowledge-Augmented Language Model and Its Application to Unsupervised Named-Entity Recognition. </span><em>Angli Liu, Jingfei Du and Veselin Stoyanov</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers4" id="session-3d"><div id="expander"></div><a href="#" class="session-title">3D: Machine Translation</a><br/><span class="session-time" title="Monday, June 03, 2019">17:00 &ndash; 18:30</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-3d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-3d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Marine Carpuat</td></tr>
<tr id="paper" paper-id="247"><td id="paper-time">17:00&ndash;17:18</td><td><span class="paper-title">Syntax-Enhanced Neural Machine Translation with Syntax-Aware Word Representations. </span><em>Meishan Zhang, Zhenghua Li, Guohong Fu and Min Zhang</em></td></tr>
<tr id="paper" paper-id="2062"><td id="paper-time">17:18&ndash;17:36</td><td><span class="paper-title">Competence-based Curriculum Learning for Neural Machine Translation. </span><em>Emmanouil Antonios Platanios, Otilia Stretcu, Graham Neubig, Barnabas Poczos and Tom Mitchell</em></td></tr>
<tr id="paper" paper-id="1655"><td id="paper-time">17:36&ndash;17:54</td><td><span class="paper-title">Extract and Edit: An Alternative to Back-Translation for Unsupervised Neural Machine Translation. </span><em>Jiawei Wu, Xin Wang and William Yang Wang</em></td></tr>
<tr id="paper" paper-id="1953"><td id="paper-time">17:54&ndash;18:12</td><td><span class="paper-title">Consistency by Agreement in Zero-Shot Neural Machine Translation. </span><em>Maruan Al-Shedivat and Ankur Parikh</em></td></tr>
<tr id="paper" paper-id="1006"><td id="paper-time">18:12&ndash;18:30</td><td><span class="paper-title">Modeling Recurrence for Transformer. </span><em>Jie Hao, Xing Wang, Baosong Yang, Longyue Wang, Jinfeng Zhang and Zhaopeng Tu</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers5" id="session-3e"><div id="expander"></div><a href="#" class="session-title">3E: Dialogue</a><br/><span class="session-time" title="Monday, June 03, 2019">17:00 &ndash; 18:30</span><br/><span class="session-location btn btn--location">Northstar A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-3e-selector"> Choose All</a><a href="#" class="session-deselector" id="session-3e-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Sujith Ravi</td></tr>
<tr id="paper" paper-id="543"><td id="paper-time">17:00&ndash;17:18</td><td><span class="paper-title">Rethinking Action Spaces for Reinforcement Learning in End-to-end Dialog Agents with Latent Variable Models. </span><em>Tiancheng Zhao, Kaige Xie and Maxine Eskenazi</em></td></tr>
<tr id="paper" paper-id="555"><td id="paper-time">17:18&ndash;17:36</td><td><span class="paper-title">Skeleton-to-Response: Dialogue Generation Guided by Retrieval Memory. </span><em>Deng Cai, Yan Wang, Wei Bi, Zhaopeng Tu, Xiaojiang Liu, Wai Lam and Shuming Shi</em></td></tr>
<tr id="paper" paper-id="2208"><td id="paper-time">17:36&ndash;17:54</td><td><span class="paper-title">Jointly Optimizing Diversity and Relevance in Neural Response Generation. </span><em>Xiang Gao, Sungjin Lee, Yizhe Zhang, Chris Brockett, Michel Galley, Jianfeng Gao and Bill Dolan</em></td></tr>
<tr id="paper" paper-id="2314"><td id="paper-time">17:54&ndash;18:12</td><td><span class="paper-title">Disentangling Language and Knowledge in Task-Oriented Dialogs. </span><em>Dinesh Raghu, Nikhil Gupta and  Mausam</em></td></tr>
<tr id="paper" paper-id="2484-tacl"><td id="paper-time">18:12&ndash;18:30</td><td><span class="paper-title">DREAM: A Challenge Dataset and Models for Dialogue-Based Reading Comprehension. </span><em>Kai Sun, Dian Yu, Jianshu Chen, Dong Yu, Yejin Choi and Claire Cardie</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-posters" id="session-poster-3"><div id="expander"></div><a href="#" class="session-title">3F: Applications, Social Media, Biomedical NLP & Clinical Text Processing (Posters & Demos) </a><br/><span class="session-time" title="Monday, June 03, 2019">17:00 &ndash; 18:30</span><br/><span class="session-location btn btn--location">Hyatt Exhibit Hall</span><div class="poster-session-details"><br/><table class="poster-table">
<tr><td><span class="poster-type">Applications</span></td></tr>
<tr id="poster" poster-id="459"><td><span class="poster-title">Tensorized Self-Attention: Efficiently Modeling Pairwise and Global Dependencies Together. </span><em>Tao Shen, Tianyi Zhou, Guodong Long, Jing Jiang and Chengqi Zhang</em></td></tr>
<tr id="poster" poster-id="464"><td><span class="poster-title">WiC: the Word-in-Context Dataset for Evaluating Context-Sensitive Meaning Representations. </span><em>Mohammad Taher Pilehvar and Jose Camacho-Collados</em></td></tr>
<tr id="poster" poster-id="1434"><td><span class="poster-title">Does My Rebuttal Matter? Insights from a Major NLP Conference. </span><em>Yang Gao, Steffen Eger, Ilia Kuznetsov, Iryna Gurevych and Yusuke Miyao</em></td></tr>
<tr id="poster" poster-id="1760"><td><span class="poster-title">Casting Light on Invisible Cities: Computationally Engaging with Literary Criticism. </span><em>Shufan Wang and Mohit Iyyer</em></td></tr>
<tr id="poster" poster-id="1907"><td><span class="poster-title">PAWS: Paraphrase Adversaries from Word Scrambling. </span><em>Yuan Zhang, Jason Baldridge and Luheng He</em></td></tr>
<tr id="poster" poster-id="2251"><td><span class="poster-title">Cross-Corpora Evaluation and Analysis of Grammatical Error Correction Models — Is Single-Corpus Evaluation Enough?. </span><em>Masato Mita, Tomoya Mizumoto, Masahiro Kaneko, Ryo Nagata and Kentaro Inui</em></td></tr>
<tr id="poster" poster-id="2337"><td><span class="poster-title">Star-Transformer. </span><em>Qipeng Guo, Xipeng Qiu, Pengfei Liu, Yunfan Shao, Xiangyang Xue and Zheng Zhang</em></td></tr>
<tr id="poster" poster-id="20-srw"><td><span class="poster-title">SEDTWik: Segmentation-based Event Detection from Tweets Using Wikipedia. </span><em>Keval Morabia, Neti Lalita Bhanu Murthy, Aruna Malapati and Surender Samant</em></td></tr>
<tr><td><span class="poster-type">Social Media</span></td></tr>
<tr id="poster" poster-id="101"><td><span class="poster-title">Adaptation of Hierarchical Structured Models for Speech Act Recognition in Asynchronous Conversation. </span><em>Tasnim Mohiuddin, Thanh-Tung Nguyen and Shafiq Joty</em></td></tr>
<tr id="poster" poster-id="591"><td><span class="poster-title">From legal to technical concept: Towards an automated classification of German political Twitter postings as criminal offenses. </span><em>Frederike Zufall, Tobias Horsmann and Torsten Zesch</em></td></tr>
<tr id="poster" poster-id="655"><td><span class="poster-title">Joint Multi-Label Attention Networks for Social Text Annotation. </span><em>Hang Dong, Wei Wang, Kaizhu Huang and Frans Coenen</em></td></tr>
<tr id="poster" poster-id="754"><td><span class="poster-title">Multi-Channel Convolutional Neural Network for Twitter Emotion and Sentiment Recognition. </span><em>Jumayel Islam, Robert E. Mercer and Lu Xiao</em></td></tr>
<tr id="poster" poster-id="1010"><td><span class="poster-title">Detecting Cybersecurity Events from Noisy Short Text. </span><em>Semih Yagcioglu, Mehmet saygin Seyfioglu, Begum Citamak, Batuhan Bardak, Seren Guldamlasioglu, Azmi Yuksel and Emin Islam Tatli</em></td></tr>
<tr id="poster" poster-id="1265"><td><span class="poster-title">White-to-Black: Efficient Distillation of Black-Box Adversarial Attacks. </span><em>Yotam Gil, Yoav Chai, Or Gorodissky and Jonathan Berant</em></td></tr>
<tr id="poster" poster-id="1269"><td><span class="poster-title">Analyzing the Perceived Severity of Cybersecurity Threats Reported on Social Media. </span><em>Shi Zong, Alan Ritter, Graham Mueller and Evan Wright</em></td></tr>
<tr id="poster" poster-id="1410"><td><span class="poster-title">Fake News Detection using Deep Markov Random Fields. </span><em>Duc Minh Nguyen, Tien Huu Do, Robert Calderbank and Nikos Deligiannis</em></td></tr>
<tr id="poster" poster-id="1499"><td><span class="poster-title">Issue Framing in Online Discussion Fora. </span><em>Mareike Hartmann, Tallulah Jansen, Isabelle Augenstein and Anders Søgaard</em></td></tr>
<tr id="poster" poster-id="1512"><td><span class="poster-title">Vector of Locally Aggregated Embeddings for Text Representation. </span><em>Hadi Amiri and Mitra Mohtarami</em></td></tr>
<tr id="poster" poster-id="1873"><td><span class="poster-title">Predicting the Type and Target of Offensive Posts in Social Media. </span><em>Marcos Zampieri, Shervin Malmasi, Preslav Nakov, Sara Rosenthal, Noura Farra and Ritesh Kumar</em></td></tr>
<tr><td><span class="poster-type">Biomedical NLP & Clinical Text Processing</span></td></tr>
<tr id="poster" poster-id="152"><td><span class="poster-title">Biomedical Event Extraction based on Knowledge-driven Tree-LSTM. </span><em>Diya Li, Lifu Huang, Heng Ji and Jiawei Han</em></td></tr>
<tr id="poster" poster-id="161"><td><span class="poster-title">Detecting cognitive impairments by agreeing on interpretations of linguistic features. </span><em>Zining Zhu, Jekaterina Novikova and Frank Rudzicz</em></td></tr>
<tr id="poster" poster-id="232"><td><span class="poster-title">Relation Extraction using Explicit Context Conditioning. </span><em>Gaurav Singh and Parminder Bhatia</em></td></tr>
<tr id="poster" poster-id="279"><td><span class="poster-title">Conversation Model Fine-Tuning for Classifying Client Utterances in Counseling Dialogues. </span><em>Sungjoon Park, Donghyun Kim and Alice Oh</em></td></tr>
<tr id="poster" poster-id="317"><td><span class="poster-title">Using Similarity Measures to Select Pretraining Data for NER. </span><em>Xiang Dai, Sarvnaz Karimi, Ben Hachey and Cecile Paris</em></td></tr>
<tr id="poster" poster-id="384"><td><span class="poster-title">Predicting Annotation Difficulty to Improve Task Routing and Model Performance for Biomedical Information Extraction. </span><em>Yinfei Yang, Oshin Agarwal, Chris Tar, Byron C. Wallace and Ani Nenkova</em></td></tr>
<tr id="poster" poster-id="1938"><td><span class="poster-title">Detecting Depression in Social Media using Fine-Grained Emotions. </span><em>Mario Ezra Aragon, Adrian Pastor Lopez Monroy, Luis Carlos Gonzalez Gurrola and Manuel Montes-y-Gomez</em></td></tr>
<tr id="poster" poster-id="2435"><td><span class="poster-title">A Silver Standard Corpus of Human Phenotype-Gene Relations. </span><em>Diana Sousa, Andre Lamurias and Francisco M Couto</em></td></tr>
<tr id="poster" poster-id="53-srw"><td><span class="poster-title">Kickstarting NLP for the Whole-person Function Domain with Representation Learning and Data Analysis. </span><em>Denis Newman-Griffis</em></td></tr>
<tr id="poster" poster-id="10-demos"><td><span class="poster-title">compare-mt: A Tool for Holistic Comparison of Language Generation Systems. </span><em>Graham Neubig, Zi-Yi Dou, Junjie Hu, Paul Michel, Danish Pruthi and Xinyi Wang</em></td></tr>
<tr id="poster" poster-id="25-demos"><td><span class="poster-title">Eidos, INDRA,  Delphi: From Free Text to Executable Causal Models. </span><em>Rebecca Sharp, Adarsh Pyarelal, Benjamin Gyori, Keith Alcock, Egoitz Laparra, Marco A. Valenzuela-Escárcega, Ajay Nagesh, Vikas Yadav, John Bachman, Zheng Tang, Heather Lent, Fan Luo, Mithun Paul, Steven Bethard, Kobus Barnard, Clayton Morrison and Mihai Surdeanu</em></td></tr>
<tr id="poster" poster-id="16-demos"><td><span class="poster-title">fairseq: A Fast, Extensible Toolkit for Sequence Modeling. </span><em>Myle Ott, Sergey Edunov, Alexei Baevski, Angela Fan, Sam Gross, Nathan Ng, David Grangier and Michael Auli</em></td></tr>
<tr id="poster" poster-id="21-demos"><td><span class="poster-title">FLAIR: An Easy-to-Use Framework for State-of-the-Art NLP. </span><em>Alan Akbik, Tanja Bergmann, Duncan Blythe, Kashif Rasul, Stefan Schweter and Roland Vollgraf</em></td></tr>
<tr id="poster" poster-id="51-demos"><td><span class="poster-title">ChatEval: A Tool for Chatbot Evaluation. </span><em>Joao Sedoc, Daphne Ippolito, Arun Kirubarajan, Jai Thirani, Lyle Ungar and Chris Callison-Burch</em></td></tr>
<tr id="poster" poster-id="35-demos"><td><span class="poster-title">LeafNATS: An Open-Source Toolkit and Live Demo System for Neural Abstractive Text Summarization. </span><em>Tian Shi, Ping Wang and Chandan K. Reddy</em></td></tr>
</table>
</div>
</div>
</div>
<div class="day" id="day-3">Tuesday, June 04, 2019</div>
<div class="session-box" id="session-box-4">
<div class="session-header" id="session-header-4">Long Orals / Long & Short Posters</div>
<div class="session session-expandable session-papers1" id="session-4a"><div id="expander"></div><a href="#" class="session-title">4A: Phonology  & Morphology</a><br/><span class="session-time" title="Tuesday, June 04, 2019">9:00 &ndash; 10:30</span><br/><span class="session-location btn btn--location">Nicollet A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-4a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-4a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Greg Kondrak</td></tr>
<tr id="paper" paper-id="303"><td id="paper-time">9:00&ndash;9:18</td><td><span class="paper-title">Improving Lemmatization of Non-Standard Languages with Joint Learning. </span><em>Enrique Manjavacas, Ákos Kádár and Mike Kestemont</em></td></tr>
<tr id="paper" paper-id="658"><td id="paper-time">9:18&ndash;9:36</td><td><span class="paper-title">One Size Does Not Fit All: Comparing NMT Representations of Different Granularities. </span><em>Nadir Durrani, Fahim Dalvi, Hassan Sajjad, Yonatan Belinkov and Preslav Nakov</em></td></tr>
<tr id="paper" paper-id="805"><td id="paper-time">9:36&ndash;9:54</td><td><span class="paper-title">A Simple Joint Model for Improved Contextual Neural Lemmatization. </span><em>Chaitanya Malaviya, Shijie Wu and Ryan Cotterell</em></td></tr>
<tr id="paper" paper-id="1257"><td id="paper-time">9:54&ndash;10:12</td><td><span class="paper-title">A Probabilistic Generative Model of Linguistic Typology. </span><em>Johannes Bjerva, Yova Kementchedjhieva, Ryan Cotterell and Isabelle Augenstein</em></td></tr>
<tr id="paper" paper-id="2348"><td id="paper-time">10:12&ndash;10:30</td><td><span class="paper-title">Quantifying the morphosyntactic content of Brown Clusters. </span><em>Manuel Ciosici, Leon Derczynski and Ira Assent</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers2" id="session-4b"><div id="expander"></div><a href="#" class="session-title">4B: Multilingual NLP</a><br/><span class="session-time" title="Tuesday, June 04, 2019">9:00 &ndash; 10:30</span><br/><span class="session-location btn btn--location">Nicollet D</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-4b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-4b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Ekaterina Shutova</td></tr>
<tr id="paper" paper-id="231"><td id="paper-time">9:00&ndash;9:18</td><td><span class="paper-title">Analyzing Bayesian Crosslingual Transfer in Topic Models. </span><em>Shudong Hao and Michael J. Paul</em></td></tr>
<tr id="paper" paper-id="994"><td id="paper-time">9:18&ndash;9:36</td><td><span class="paper-title">Recursive Subtree Composition in LSTM-Based Dependency Parsing. </span><em>Miryam de Lhoneux, Miguel Ballesteros and Joakim Nivre</em></td></tr>
<tr id="paper" paper-id="1044"><td id="paper-time">9:36&ndash;9:54</td><td><span class="paper-title">Cross-lingual CCG Induction. </span><em> and Kilian Evang</em></td></tr>
<tr id="paper" paper-id="1933"><td id="paper-time">9:54&ndash;10:12</td><td><span class="paper-title">Density Matching for Bilingual Word Embedding. </span><em>Chunting Zhou, Xuezhe Ma, Di Wang and Graham Neubig</em></td></tr>
<tr id="paper" paper-id="2113"><td id="paper-time">10:12&ndash;10:30</td><td><span class="paper-title">Cross-Lingual Alignment of Contextual Word Embeddings, with Applications to Zero-shot Dependency Parsing. </span><em>Tal Schuster, Ori Ram, Regina Barzilay and Amir Globerson</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers3" id="session-4c"><div id="expander"></div><a href="#" class="session-title">4C: Social Media</a><br/><span class="session-time" title="Tuesday, June 04, 2019">9:00 &ndash; 10:30</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-4c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-4c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Xiaodan Zhu</td></tr>
<tr id="paper" paper-id="321"><td id="paper-time">9:00&ndash;9:18</td><td><span class="paper-title">Early Rumour Detection. </span><em>Kaimin Zhou, Chang Shu, Binyang Li and Jey Han Lau</em></td></tr>
<tr id="paper" paper-id="449"><td id="paper-time">9:18&ndash;9:36</td><td><span class="paper-title">Microblog Hashtag Generation via Encoding Conversation Contexts. </span><em>Yue Wang, Jing Li, Irwin King, Michael R. Lyu and Shuming Shi</em></td></tr>
<tr id="paper" paper-id="1200"><td id="paper-time">9:36&ndash;9:54</td><td><span class="paper-title">Text Processing Like Humans Do: Visually Attacking and Shielding NLP Systems. </span><em>Steffen Eger, Gözde Gül Şahin, Andreas Rücklé, Ji-Ung Lee, Claudia Schulz, Mohsen Mesgar, Krishnkant Swarnkar, Edwin Simpson and Iryna Gurevych</em></td></tr>
<tr id="paper" paper-id="1616"><td id="paper-time">9:54&ndash;10:12</td><td><span class="paper-title">Something’s Brewing! Early Prediction of Controversy-causing Posts from Discussion Features. </span><em>Jack Hessel and Lillian Lee</em></td></tr>
<tr id="paper" paper-id="1962"><td id="paper-time">10:12&ndash;10:30</td><td><span class="paper-title">No Permanent Friends or Enemies: Tracking Relationships between Nations from News. </span><em>Xiaochuang Han, Eunsol Choi and Chenhao Tan</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers4" id="session-4d"><div id="expander"></div><a href="#" class="session-title">4D: Generation</a><br/><span class="session-time" title="Tuesday, June 04, 2019">9:00 &ndash; 10:30</span><br/><span class="session-location btn btn--location">Northstar A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-4d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-4d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Ion Androutsopoulos</td></tr>
<tr id="paper" paper-id="1297"><td id="paper-time">9:00&ndash;9:18</td><td><span class="paper-title">Improving Human Text Comprehension through Semi-Markov CRF-based Neural Section Title Generation. </span><em>Sebastian Gehrmann, Steven Layne and Franck Dernoncourt</em></td></tr>
<tr id="paper" paper-id="1807"><td id="paper-time">9:18&ndash;9:36</td><td><span class="paper-title">Unifying Human and Statistical Evaluation for Natural Language Generation. </span><em>Tatsunori Hashimoto, Hugh Zhang and Percy Liang</em></td></tr>
<tr id="paper" paper-id="1909"><td id="paper-time">9:36&ndash;9:54</td><td><span class="paper-title">What makes a good conversation? How controllable attributes affect human judgments. </span><em>Abigail See, Stephen Roller, Douwe Kiela and Jason Weston</em></td></tr>
<tr id="paper" paper-id="1923"><td id="paper-time">9:54&ndash;10:12</td><td><span class="paper-title">An Empirical Investigation of Global and Local Normalization for Recurrent Neural Sequence Models Using a Continuous Relaxation to Beam Search. </span><em>Kartik Goyal, Chris Dyer and Taylor Berg-Kirkpatrick</em></td></tr>
<tr id="paper" paper-id="2045"><td id="paper-time">10:12&ndash;10:30</td><td><span class="paper-title">Pun Generation with Surprise. </span><em>He He, Nanyun Peng and Percy Liang</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers5" id="session-4e"><div id="expander"></div><a href="#" class="session-title">4E: Industry: Real World Challenges</a><br/><span class="session-time" title="Tuesday, June 04, 2019">9:00 &ndash; 10:30</span><br/><span class="session-location btn btn--location">Greenway</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-4e-selector"> Choose All</a><a href="#" class="session-deselector" id="session-4e-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Nizar Habash</td></tr>
<tr id="paper" paper-id="4036-industry"><td id="paper-time">09:00&ndash;09:18</td><td><span class="paper-title">Enabling Real-time Neural IME with Incremental Vocabulary Selection. </span><em>Jiali Yao, Raphael Shu, Xinjian Li, Katsutoshi Ohtsuki and Hideki Nakayama</em></td></tr>
<tr id="paper" paper-id="4075-industry"><td id="paper-time">09:18&ndash;09:36</td><td><span class="paper-title">Locale-agnostic Universal Domain Classification Model in Spoken Language Understanding. </span><em>Jihwan Lee, Ruhi Sarikaya and Young-Bum Kim</em></td></tr>
<tr id="paper" paper-id="4055-industry"><td id="paper-time">09:36&ndash;09:54</td><td><span class="paper-title">Practical Semantic Parsing for Spoken Language Understanding. </span><em>Marco Damonte, Rahul Goel and Tagyoung Chung</em></td></tr>
<tr id="paper" paper-id="4116-industry"><td id="paper-time">09:54&ndash;10:12</td><td><span class="paper-title">Fast Prototyping a Dialogue Comprehension System for Nurse-Patient Conversations on Symptom Monitoring. </span><em>Zhengyuan Liu, Hazel Lim, Nur Farah Ain Suhaimi, Shao Chuen Tong, Sharon Ong, Angela Ng, Sheldon Lee, Michael R. Macdonald, Savitha Ramasamy, Pavitra Krishnaswamy, Wai Leng Chow and Nancy F. Chen</em></td></tr>
<tr id="paper" paper-id="4015-industry"><td id="paper-time">10:12&ndash;10:30</td><td><span class="paper-title">Graph Convolution for Multimodal Information Extraction from Visually Rich Documents. </span><em>Xiaojing Liu, Feiyu Gao, Qiong Zhang and Huasha Zhao</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-posters" id="session-poster-4"><div id="expander"></div><a href="#" class="session-title">4F: Discourse, Information Retrieval, Machine Translation, Vision  & Robotics (Posters) </a><br/><span class="session-time" title="Tuesday, June 04, 2019">9:00 &ndash; 10:30</span><br/><span class="session-location btn btn--location">Hyatt Exhibit Hall</span><div class="poster-session-details"><br/><table class="poster-table">
<tr><td><span class="poster-type">Discourse</span></td></tr>
<tr id="poster" poster-id="348"><td><span class="poster-title">Single Document Summarization as Tree Induction. </span><em>Yang Liu, Ivan Titov and Mirella Lapata</em></td></tr>
<tr id="poster" poster-id="493"><td><span class="poster-title">Fixed That for You: Generating Contrastive Claims with Semantic Edits. </span><em>Christopher Hidey and Kathy McKeown</em></td></tr>
<tr id="poster" poster-id="1443"><td><span class="poster-title">Box of Lies: Multimodal Deception Detection in Dialogues. </span><em>Felix Soldner, Verónica Pérez-Rosas and Rada Mihalcea</em></td></tr>
<tr id="poster" poster-id="1445"><td><span class="poster-title">A Crowdsourced Corpus of Multiple Judgments and Disagreement on Anaphoric Interpretation. </span><em>Massimo Poesio, Jon Chamberlain, Silviu Paun, Juntao Yu, Alexandra Uma and Udo Kruschwitz</em></td></tr>
<tr id="poster" poster-id="1615"><td><span class="poster-title">A Streamlined Method for Sourcing Discourse-level Argumentation Annotations from the Crowd. </span><em>Tristan Miller, Maria Sukhareva and Iryna Gurevych</em></td></tr>
<tr id="poster" poster-id="1634"><td><span class="poster-title">Unsupervised Dialog Structure Learning. </span><em>Weiyan Shi, Tiancheng Zhao and Zhou Yu</em></td></tr>
<tr id="poster" poster-id="2180"><td><span class="poster-title">Modeling Document-level Causal Structures for Event Causal Relation Identification. </span><em>Lei Gao, Prafulla Kumar Choubey and Ruihong Huang</em></td></tr>
<tr id="poster" poster-id="2483-tacl"><td><span class="poster-title">Planning, Inference, and Pragmatics in Sequential Language Games. </span><em>Fereshte Khani, Noah D. Goodman and Percy Liang</em></td></tr>
<tr><td><span class="poster-type">Information Retrieval</span></td></tr>
<tr id="poster" poster-id="1272"><td><span class="poster-title">Hierarchical User and Item Representation with Three-Tier Attention for Recommendation. </span><em>Chuhan Wu, Fangzhao Wu, Junxin Liu and Yongfeng Huang</em></td></tr>
<tr id="poster" poster-id="1274"><td><span class="poster-title">Text Similarity Estimation Based on Word Embeddings and Matrix Norms for Targeted Marketing. </span><em>Tim vor der Brück and Marc Pouly</em></td></tr>
<tr id="poster" poster-id="1321"><td><span class="poster-title">Glocal: Incorporating Global Information in Local Convolution for Keyphrase Extraction. </span><em>Animesh Prasad and Min-Yen Kan</em></td></tr>
<tr id="poster" poster-id="1537"><td><span class="poster-title">A Study of Latent Structured Prediction Approaches to Passage Reranking. </span><em>Iryna Haponchyk and Alessandro Moschitti</em></td></tr>
<tr id="poster" poster-id="1885"><td><span class="poster-title">Combining Distant and Direct Supervision for Neural Relation Extraction. </span><em>Iz Beltagy, Kyle Lo and Waleed Ammar</em></td></tr>
<tr id="poster" poster-id="2412"><td><span class="poster-title">Tweet Stance Detection Using an Attention based Neural Ensemble Model. </span><em>Umme Aymun Siddiqua, Abu Nowshed Chy and Masaki Aono</em></td></tr>
<tr><td><span class="poster-type">Machine Translation</span></td></tr>
<tr id="poster" poster-id="1242"><td><span class="poster-title">Word Embedding-Based Automatic MT Evaluation Metric using Word Position Information. </span><em>Hiroshi Echizen’ya, Kenji Araki and Eduard Hovy</em></td></tr>
<tr id="poster" poster-id="1633"><td><span class="poster-title">Learning to Stop in Structured Prediction for Neural Machine Translation. </span><em>Mingbo Ma, Renjie Zheng and Liang Huang</em></td></tr>
<tr id="poster" poster-id="1657"><td><span class="poster-title">Learning Unsupervised Multilingual Word Embeddings with Incremental Multilingual Hubs. </span><em>Geert Heyman, Bregt Verreet, Ivan Vulić and Marie-Francine Moens</em></td></tr>
<tr id="poster" poster-id="1790"><td><span class="poster-title">Curriculum Learning for Domain Adaptation in Neural Machine Translation. </span><em>Xuan Zhang, Pamela Shapiro, Gaurav Kumar, Paul McNamee, Marine Carpuat and Kevin Duh</em></td></tr>
<tr id="poster" poster-id="2010"><td><span class="poster-title">Improving Robustness of Machine Translation with Synthetic Noise. </span><em>Vaibhav Vaibhav, Sumeet Singh, Craig Stewart and Graham Neubig</em></td></tr>
<tr id="poster" poster-id="2060"><td><span class="poster-title">Non-Parametric Adaptation for Neural Machine Translation. </span><em>Ankur Bapna and Orhan Firat</em></td></tr>
<tr id="poster" poster-id="2460"><td><span class="poster-title">Online Distilling from Checkpoints for Neural Machine Translation. </span><em>Hao-Ran Wei, Shujian Huang, Ran Wang, Xin-Yu Dai and Jiajun Chen</em></td></tr>
<tr><td><span class="poster-type">Vision  & Robotics</span></td></tr>
<tr id="poster" poster-id="607"><td><span class="poster-title">Value-based Search in Execution Space for Mapping Instructions to Programs. </span><em>Dor Muhlgay, Jonathan Herzig and Jonathan Berant</em></td></tr>
<tr id="poster" poster-id="723"><td><span class="poster-title">VQD: Visual Query Detection In Natural Scenes. </span><em>Manoj Acharya, Karan Jariwala and Christopher Kanan</em></td></tr>
<tr id="poster" poster-id="730"><td><span class="poster-title">Improving Natural Language Interaction with Robots Using Advice. </span><em>Nikhil Mehta and Dan Goldwasser</em></td></tr>
<tr id="poster" poster-id="1299"><td><span class="poster-title">Generating Knowledge Graph Paths from Textual Definitions using Sequence-to-Sequence Models. </span><em>Victor Prokhorov, Mohammad Taher Pilehvar and Nigel Collier</em></td></tr>
<tr id="poster" poster-id="1467"><td><span class="poster-title">Shifting the Baseline: Single Modality Performance on Visual Navigation  QA. </span><em>Jesse Thomason, Daniel Gordon and Yonatan Bisk</em></td></tr>
<tr id="poster" poster-id="2216"><td><span class="poster-title">ExCL: Extractive Clip Localization Using Natural Language Descriptions. </span><em>Soham Ghosh, Anuva Agarwal, Zarana Parekh and Alexander Hauptmann</em></td></tr>
</table>
</div>
</div>
</div>
<div class="session session-break session-plenary" id="session-break-9"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Tuesday, June 04, 2019">10:30 &ndash; 11:00</span></div>
<div class="session-box" id="session-box-5">
<div class="session-header" id="session-header-5">Short Orals / Long & Short Posters / Demos</div>
<div class="session session-expandable session-papers1" id="session-5a"><div id="expander"></div><a href="#" class="session-title">5A: Multilingual NLP</a><br/><span class="session-time" title="Tuesday, June 04, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Nicollet D</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-5a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-5a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Valia Kordoni</td></tr>
<tr id="paper" paper-id="495"><td id="paper-time">11:00&ndash;11:15</td><td><span class="paper-title">Detecting dementia in Mandarin Chinese using transfer learning from a parallel corpus. </span><em>Bai Li, Yi-Te Hsu and Frank Rudzicz</em></td></tr>
<tr id="paper" paper-id="1331"><td id="paper-time">11:15&ndash;11:30</td><td><span class="paper-title">Cross-lingual Visual Verb Sense Disambiguation. </span><em>Spandana Gella, Desmond Elliott and Frank Keller</em></td></tr>
<tr id="paper" paper-id="1338"><td id="paper-time">11:30&ndash;11:45</td><td><span class="paper-title">Subword-Level Language Identification for Intra-Word Code-Switching. </span><em>Manuel Mager, Özlem Çetinoğlu and Katharina Kann</em></td></tr>
<tr id="paper" paper-id="1412"><td id="paper-time">11:45&ndash;12:00</td><td><span class="paper-title">MuST-C: a Multilingual Speech Translation Corpus. </span><em>Mattia A. Di Gangi, Roldano Cattoni, Luisa Bentivogli, Matteo Negri and Marco Turchi</em></td></tr>
<tr id="paper" paper-id="1520"><td id="paper-time">12:00&ndash;12:15</td><td><span class="paper-title">Contextualization of Morphological Inflection. </span><em>Ekaterina Vylomova, Ryan Cotterell, Trevor Cohn, Timothy Baldwin and Jason Eisner</em></td></tr>
<tr id="paper" paper-id="1668"><td id="paper-time">12:15&ndash;12:30</td><td><span class="paper-title">A Robust Abstractive System for Cross-Lingual Summarization. </span><em>Jessica Ouyang, Boya Song and Kathy McKeown</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers2" id="session-5b"><div id="expander"></div><a href="#" class="session-title">5B: Machine Translation</a><br/><span class="session-time" title="Tuesday, June 04, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-5b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-5b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Daisuke Kawahara</td></tr>
<tr id="paper" paper-id="325"><td id="paper-time">11:00&ndash;11:15</td><td><span class="paper-title">Improving Neural Machine Translation with Neural Syntactic Distance. </span><em>Chunpeng Ma, Akihiro Tamura, Masao Utiyama, Eiichiro Sumita and Tiejun Zhao</em></td></tr>
<tr id="paper" paper-id="1534"><td id="paper-time">11:15&ndash;11:30</td><td><span class="paper-title">Measuring Immediate Adaptation Performance for Neural Machine Translation. </span><em>Patrick Simianer, Joern Wuebker and John DeNero</em></td></tr>
<tr id="paper" paper-id="1614"><td id="paper-time">11:30&ndash;11:45</td><td><span class="paper-title">Differentiable Sampling with Flexible Reference Word Order for Neural Machine Translation. </span><em>Weijia Xu, Xing Niu and Marine Carpuat</em></td></tr>
<tr id="paper" paper-id="1739"><td id="paper-time">11:45&ndash;12:00</td><td><span class="paper-title">Reinforcement Learning based Curriculum Optimization for Neural Machine Translation. </span><em>Gaurav Kumar, George Foster, Colin Cherry and Maxim Krikun</em></td></tr>
<tr id="paper" paper-id="1956"><td id="paper-time">12:00&ndash;12:15</td><td><span class="paper-title">Overcoming Catastrophic Forgetting During Domain Adaptation of Neural Machine Translation. </span><em>Brian Thompson, Jeremy Gwinnup, Huda Khayrallah, Kevin Duh and Philipp Koehn</em></td></tr>
<tr id="paper" paper-id="32-srw"><td id="paper-time">12:15&ndash;12:30</td><td><span class="paper-title">Multimodal Machine Translation with Embedding Prediction. </span><em>Tosho Hirasawa, Hayahide Yamagishi, Yukio Matsumura and Mamoru Komachi</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers3" id="session-5c"><div id="expander"></div><a href="#" class="session-title">5C: Social Media</a><br/><span class="session-time" title="Tuesday, June 04, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Greenway</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-5c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-5c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Chenhao Tan</td></tr>
<tr id="paper" paper-id="1381"><td id="paper-time">11:00&ndash;11:15</td><td><span class="paper-title">Short-Term Meaning Shift: A Distributional Exploration. </span><em>Marco Del Tredici, Raquel Fernández and Gemma Boleda</em></td></tr>
<tr id="paper" paper-id="617"><td id="paper-time">11:15&ndash;11:30</td><td><span class="paper-title">Detecting Derogatory Compounds – An Unsupervised Approach. </span><em>Michael Wiegand, Maximilian Wolf and Josef Ruppenhofer</em></td></tr>
<tr id="paper" paper-id="133"><td id="paper-time">11:30&ndash;11:45</td><td><span class="paper-title">Personalized Neural Embeddings for Collaborative Filtering with Text. </span><em> and Guangneng Hu</em></td></tr>
<tr id="paper" paper-id="1570"><td id="paper-time">11:45&ndash;12:00</td><td><span class="paper-title">An Embarrassingly Simple Approach for Transfer Learning from Pretrained Language Models. </span><em>Alexandra Chronopoulou, Christos Baziotis and Alexandros Potamianos</em></td></tr>
<tr id="paper" paper-id="1815"><td id="paper-time">12:00&ndash;12:15</td><td><span class="paper-title">Incorporating Emoji Descriptions Improves Tweet Classification. </span><em>Abhishek Singh, Eduardo Blanco and Wei Jin</em></td></tr>
<tr id="paper" paper-id="2454"><td id="paper-time">12:15&ndash;12:30</td><td><span class="paper-title">Modeling Personal Biases in Language Use by Inducing Personalized Word Embeddings. </span><em>Daisuke Oba, Naoki Yoshinaga, Shoetsu Sato, Satoshi Akasaki and Masashi Toyoda</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers4" id="session-5d"><div id="expander"></div><a href="#" class="session-title">5D: Text Analysis</a><br/><span class="session-time" title="Tuesday, June 04, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Northstar A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-5d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-5d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Saif Mohammad</td></tr>
<tr id="paper" paper-id="590"><td id="paper-time">11:00&ndash;11:15</td><td><span class="paper-title">Multi-Task Ordinal Regression for Jointly Predicting the Trustworthiness and the Leading Political Ideology of News Media. </span><em>Ramy Baly, Georgi Karadzhov, Abdelrhman Saleh, James Glass and Preslav Nakov</em></td></tr>
<tr id="paper" paper-id="2379"><td id="paper-time">11:15&ndash;11:30</td><td><span class="paper-title">Joint Detection and Location of English Puns. </span><em>Yanyan Zou and Wei Lu</em></td></tr>
<tr id="paper" paper-id="1603"><td id="paper-time">11:30&ndash;11:45</td><td><span class="paper-title">Harry Potter and the Action Prediction Challenge from Natural Language. </span><em>David Vilares and Carlos Gómez-Rodríguez</em></td></tr>
<tr id="paper" paper-id="1617"><td id="paper-time">11:45&ndash;12:00</td><td><span class="paper-title">Argument Mining for Understanding Peer Reviews. </span><em>Xinyu Hua, Mitko Nikolov, Nikhil Badugu and Lu Wang</em></td></tr>
<tr id="paper" paper-id="1903"><td id="paper-time">12:00&ndash;12:15</td><td><span class="paper-title">An annotated dataset of literary entities. </span><em>David Bamman, Sejal Popat and Sheng Shen</em></td></tr>
<tr id="paper" paper-id="1363"><td id="paper-time">12:15&ndash;12:30</td><td><span class="paper-title">Abusive Language Detection with Graph Convolutional Networks. </span><em>Pushkar Mishra, Marco Del Tredici, Helen Yannakoudakis and Ekaterina Shutova</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers5" id="session-5e"><div id="expander"></div><a href="#" class="session-title">5E: Semantics</a><br/><span class="session-time" title="Tuesday, June 04, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Nicollet A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-5e-selector"> Choose All</a><a href="#" class="session-deselector" id="session-5e-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Samuel Bowman</td></tr>
<tr id="paper" paper-id="465"><td id="paper-time">11:00&ndash;11:15</td><td><span class="paper-title">On the Importance of Distinguishing Word Meaning Representations: A Case Study on Reverse Dictionary Mapping. </span><em> and Mohammad Taher Pilehvar</em></td></tr>
<tr id="paper" paper-id="1399"><td id="paper-time">11:15&ndash;11:30</td><td><span class="paper-title">Factorising AMR generation through syntax. </span><em>Kris Cao and Stephen Clark</em></td></tr>
<tr id="paper" paper-id="1456"><td id="paper-time">11:30&ndash;11:45</td><td><span class="paper-title">A Crowdsourced Frame Disambiguation Corpus with Ambiguity. </span><em>Anca Dumitrache, Lora Aroyo and Chris Welty</em></td></tr>
<tr id="paper" paper-id="1951"><td id="paper-time">11:45&ndash;12:00</td><td><span class="paper-title">Inoculation by Fine-Tuning: A Method for Analyzing Challenge Datasets. </span><em>Nelson F. Liu, Roy Schwartz and Noah A. Smith</em></td></tr>
<tr id="paper" paper-id="41-srw"><td id="paper-time">12:00&ndash;12:15</td><td><span class="paper-title">Word Polysemy Aware Document Vector Estimation. </span><em>Vivek Gupta, Ankit Saw, Harshit Gupta, Pegah Nokhiz and Partha Talukdar</em></td></tr>
<tr id="paper" paper-id="47-srw"><td id="paper-time">12:15&ndash;12:30</td><td><span class="paper-title">EQUATE : A Benchmark Evaluation Framework for Quantitative Reasoning in Natural Language Inference. </span><em>Abhilasha Ravichander, Aakanksha Naik, Carolyn Rose and Eduard Hovy</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-posters" id="session-poster-5"><div id="expander"></div><a href="#" class="session-title">5F: Information Retrieval, Generation, Question Answering & Syntax (Posters & Demos) </a><br/><span class="session-time" title="Tuesday, June 04, 2019">11:00 &ndash; 12:30</span><br/><span class="session-location btn btn--location">Hyatt Exhibit Hall</span><div class="poster-session-details"><br/><table class="poster-table">
<tr><td><span class="poster-type">Information Retrieval</span></td></tr>
<tr id="poster" poster-id="117"><td><span class="poster-title">A Capsule Network-based Embedding Model for Knowledge Graph Completion and Search Personalization. </span><em>Dai Quoc Nguyen, Thanh Vu, Tu Dinh Nguyen, Dat Quoc Nguyen and Dinh Phung</em></td></tr>
<tr id="poster" poster-id="242"><td><span class="poster-title">Partial Or Complete, That’s The Question. </span><em>Qiang Ning, Hangfeng He, Chuchu Fan and Dan Roth</em></td></tr>
<tr id="poster" poster-id="487"><td><span class="poster-title">Sequential Attention with Keyword Mask Model for Community-based Question Answering. </span><em>Jianxin Yang, Wenge Rong, Libin Shi and Zhang Xiong</em></td></tr>
<tr id="poster" poster-id="548"><td><span class="poster-title">Simple Attention-Based Representation Learning for Ranking Short Social Media Posts. </span><em>Peng Shi, Jinfeng Rao and Jimmy Lin</em></td></tr>
<tr id="poster" poster-id="707"><td><span class="poster-title">AttentiveChecker: A Bi-Directional Attention Flow Mechanism for Fact Verification. </span><em>Santosh Tokala, Vishal G, Avirup Saha and Niloy Ganguly</em></td></tr>
<tr id="poster" poster-id="856"><td><span class="poster-title">Practical, Efficient, and Customizable Active Learning for Named Entity Recognition in the Digital Humanities. </span><em>Alexander Erdmann, David Joseph Wrisley, Benjamin Allen, Christopher Brown, Sophie Cohen-Bodénès, Micha Elsner, Yukun Feng, Brian Joseph, Béatrice Joyeux-Prunel and Marie-Catherine de Marneffe</em></td></tr>
<tr id="poster" poster-id="900"><td><span class="poster-title">Doc2hash: Learning Discrete Latent variables for Documents Retrieval. </span><em>Yifei Zhang and Hao Zhu</em></td></tr>
<tr><td><span class="poster-type">Generation</span></td></tr>
<tr id="poster" poster-id="114"><td><span class="poster-title">Evaluating Text GANs as Language Models. </span><em>Guy Tevet, Gavriel Habib, Vered Shwartz and Jonathan Berant</em></td></tr>
<tr id="poster" poster-id="843"><td><span class="poster-title">Latent Code and Text-based Generative Adversarial Networks for Soft-text Generation. </span><em>Md Akmal Haidar, Mehdi Rezagholizadeh, Alan Do Omri and Ahmad Rashid</em></td></tr>
<tr id="poster" poster-id="1409"><td><span class="poster-title">Neural Text Generation from Rich Semantic Representations. </span><em>Valerie Hajdik, Jan Buys, Michael Wayne Goodman and Emily M. Bender</em></td></tr>
<tr id="poster" poster-id="1620"><td><span class="poster-title">Step-by-Step: Separating Planning from Realization in Neural Data-to-Text Generation. </span><em>Amit Moryossef, Yoav Goldberg and Ido Dagan</em></td></tr>
<tr id="poster" poster-id="1874"><td><span class="poster-title">Evaluating Rewards for Question Generation Models. </span><em>Tom Hosking and Sebastian Riedel</em></td></tr>
<tr id="poster" poster-id="1958"><td><span class="poster-title">Text Generation from Knowledge Graphs with Graph Transformers. </span><em>Rik Koncel-Kedziorski, Dhanush Bekal, Yi Luan, Mirella Lapata and Hannaneh Hajishirzi</em></td></tr>
<tr><td><span class="poster-type">Question Answering</span></td></tr>
<tr id="poster" poster-id="1354"><td><span class="poster-title">Open Information Extraction from Question-Answer Pairs. </span><em>Nikita Bhutani, Yoshihiko Suhara, Wang-Chiew Tan, Alon Halevy and H. V. Jagadish</em></td></tr>
<tr id="poster" poster-id="1485"><td><span class="poster-title">Question Answering by Reasoning Across Documents with Graph Convolutional Networks. </span><em>Nicola De Cao, Wilker Aziz and Ivan Titov</em></td></tr>
<tr id="poster" poster-id="1588"><td><span class="poster-title">A Qualitative Comparison of CoQA, SQuAD 2.0 and QuAC. </span><em> and Mark Yatskar</em></td></tr>
<tr id="poster" poster-id="1595"><td><span class="poster-title">BERT Post-Training for Review Reading Comprehension and Aspect-based Sentiment Analysis. </span><em>Hu Xu, Bing Liu, Lei Shu and Philip Yu</em></td></tr>
<tr id="poster" poster-id="1741"><td><span class="poster-title">Old is Gold: Linguistic Driven Approach for Entity and Relation Linking of Short Text. </span><em>Ahmad Sakor, Isaiah Onando Mulang’, Kuldeep Singh, Saeedeh Shekarpour, Maria Esther Vidal, Jens Lehmann and Sören Auer</em></td></tr>
<tr id="poster" poster-id="1889"><td><span class="poster-title">Be Consistent! Improving Procedural Text Comprehension using Label Consistency. </span><em>Xinya Du, Bhavana Dalvi, Niket Tandon, Antoine Bosselut, Wen-tau Yih, Peter Clark and Claire Cardie</em></td></tr>
<tr id="poster" poster-id="2084"><td><span class="poster-title">MathQA: Towards Interpretable Math Word Problem Solving with Operation-Based Formalisms. </span><em>Aida Amini, Saadia Gabriel, Shanchuan Lin, Rik Koncel-Kedziorski, Yejin Choi and Hannaneh Hajishirzi</em></td></tr>
<tr id="poster" poster-id="2203"><td><span class="poster-title">DROP: A Reading Comprehension Benchmark Requiring Discrete Reasoning Over Paragraphs. </span><em>Dheeru Dua, Yizhong Wang, Pradeep Dasigi, Gabriel Stanovsky, Sameer Singh and Matt Gardner</em></td></tr>
<tr><td><span class="poster-type">Syntax</span></td></tr>
<tr id="poster" poster-id="1283"><td><span class="poster-title">An Encoding Strategy Based Word-Character LSTM for Chinese NER. </span><em>Wei Liu, Tongge Xu, Qinghua Xu, Jiayu Song and Yueran Zu</em></td></tr>
<tr id="poster" poster-id="1344"><td><span class="poster-title">Highly Effective Arabic Diacritization using Sequence to Sequence Modeling. </span><em>Hamdy Mubarak, Ahmed Abdelali, Hassan Sajjad, Younes Samih and Kareem Darwish</em></td></tr>
<tr id="poster" poster-id="1349"><td><span class="poster-title">SC-LSTM: Learning Task-Specific Representations in Multi-Task Learning for Sequence Labeling. </span><em>Peng Lu, Ting Bai and Philippe Langlais</em></td></tr>
<tr id="poster" poster-id="1459"><td><span class="poster-title">Learning to Denoise Distantly-Labeled Data for Entity Typing. </span><em>Yasumasa Onoe and Greg Durrett</em></td></tr>
<tr id="poster" poster-id="1682"><td><span class="poster-title">A Simple and Robust Approach to Detecting Subject-Verb Agreement Errors. </span><em>Simon Flachs, Ophélie Lacroix, Marek Rei, Helen Yannakoudakis and Anders Søgaard</em></td></tr>
<tr id="poster" poster-id="1894"><td><span class="poster-title">A Grounded Unsupervised Universal Part-of-Speech Tagger for Low-Resource Languages. </span><em>Ronald Cardenas, Ying Lin, Heng Ji and Jonathan May</em></td></tr>
<tr id="poster" poster-id="1922"><td><span class="poster-title">On Difficulties of Cross-Lingual Transfer with Order Differences: A Case Study on Dependency Parsing. </span><em>Wasi Ahmad, Zhisong Zhang, Xuezhe Ma, Eduard Hovy, Kai-Wei Chang and Nanyun Peng</em></td></tr>
<tr id="poster" poster-id="2163"><td><span class="poster-title">A Multi-Task Approach for Disentangling Syntax and Semantics in Sentence Representations. </span><em>Mingda Chen, Qingming Tang, Sam Wiseman and Kevin Gimpel</em></td></tr>
<tr id="poster" poster-id="8-demos"><td><span class="poster-title">End-to-End Open-Domain Question Answering with BERTserini. </span><em>Wei Yang, Yuqing Xie, Aileen Lin, Xingyu Li, Luchen Tan, Kun Xiong, Ming Li and Jimmy Lin</em></td></tr>
<tr id="poster" poster-id="27-demos"><td><span class="poster-title">FAKTA: An Automatic End-to-End Fact Checking System. </span><em>Moin Nadeem, Wei Fang, Brian Xu, Mitra Mohtarami and James Glass</em></td></tr>
<tr id="poster" poster-id="61-demos"><td><span class="poster-title">iComposer: An Automatic Songwriting System for Chinese Popular Music. </span><em>Hsin-Pei Lee, Jhih-Sheng Fang and Wei-Yun Ma</em></td></tr>
<tr id="poster" poster-id="52-demos"><td><span class="poster-title">Plan, Write, and Revise: an Interactive System for Open-Domain Story Generation. </span><em>Seraphina Goldfarb-Tarrant, Haining Feng and Nanyun Peng</em></td></tr>
<tr id="poster" poster-id="23-demos"><td><span class="poster-title">LT Expertfinder: An Evaluation Framework for Expert Finding Methods. </span><em>Tim Fischer, Steffen Remus and Chris Biemann</em></td></tr>
<tr id="poster" poster-id="11-demos"><td><span class="poster-title">SkillBot: Towards Automatic Skill Development via User Demonstration. </span><em>Yilin Shen, Avik Ray, Hongxia Jin and Sandeep Nama</em></td></tr>
</table>
</div>
</div>
</div>
<div class="session session-break session-plenary" id="session-break-10"><span class="session-title">Lunch Break</span><br/><span class="session-time" title="Tuesday, June 04, 2019">12:30 &ndash; 14:00</span></div>
<div class="session session-expandable session-plenary"><div id="expander"></div><a href="#" class="session-title"><strong>Keynote 2: Rada Mihalcea "When the Computers Spot the Lie (and People Don’t)"</strong></a><br/><span class="session-person"><a href="https://web.eecs.umich.edu/~mihalcea/" target="_blank">Rada Mihalcea</a></span><br/><span class="session-time" title="Tuesday, June 04, 2019">14:00 &ndash; 15:00</span><br/><span class="session-location btn btn--location">Nicollet Grand Ballroom</span><div class="paper-session-details"><br/><div class="session-abstract"><p>Whether we like it or not, deception occurs everyday and everywhere: thousands of trials take place daily around the world; little white lies: “I’m busy that day!” even if your calendar is blank; news “with a twist” (a.k.a. fake news) meant to attract the readers attention or influence people in their future undertakings; misinformation in health social media posts; portrayed identities, on dating sites and elsewhere. Can a computer automatically detect deception in written accounts or in video recordings? In this talk, I will overview a decade of research in building linguistic and multimodal resources and algorithms for deception detection, targeting deceptive statements, trial videos, fake news, identity deception, and health misinformation. I will also show how these algorithms can provide insights into what makes a good lie - and thus teach us how we can spot a liar. As it turns out, computers can be trained to identify lies in many different contexts, and they can often do it better than humans do.</p></div></div></div>
<div class="session session-break session-plenary" id="session-break-11"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Tuesday, June 04, 2019">15:00 &ndash; 15:30</span></div>
<div class="session-box" id="session-box-6">
<div class="session-header" id="session-header-6">Long Orals / Long & Short Posters / Demos</div>
<div class="session session-expandable session-papers1" id="session-6a"><div id="expander"></div><a href="#" class="session-title">6A: Sentiment Analysis</a><br/><span class="session-time" title="Tuesday, June 04, 2019">15:30 &ndash; 17:00</span><br/><span class="session-location btn btn--location">Northstar A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-6a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-6a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Sara Rosenthal</td></tr>
<tr id="paper" paper-id="234"><td id="paper-time">15:30&ndash;15:48</td><td><span class="paper-title">Self-Discriminative Learning for Unsupervised Document Embedding. </span><em>Hong-You Chen, Chin-Hua Hu, Leila Wehbe and Shou-de Lin</em></td></tr>
<tr id="paper" paper-id="883"><td id="paper-time">15:48&ndash;16:06</td><td><span class="paper-title">Adaptive Convolution for Text Classification. </span><em>Byung-Ju Choi, Jun-Hyung Park and SangKeun Lee</em></td></tr>
<tr id="paper" paper-id="1649"><td id="paper-time">16:06&ndash;16:24</td><td><span class="paper-title">Zero-Shot Cross-Lingual Opinion Target Extraction. </span><em>Soufian Jebbara and Philipp Cimiano</em></td></tr>
<tr id="paper" paper-id="1979"><td id="paper-time">16:24&ndash;16:42</td><td><span class="paper-title">Adversarial Category Alignment Network for Cross-domain Sentiment Classification. </span><em>Xiaoye Qu, Zhikang Zou, Yu Cheng, Yang Yang and Pan Zhou</em></td></tr>
<tr id="paper" paper-id="2325"><td id="paper-time">16:42&ndash;17:00</td><td><span class="paper-title">Target-oriented Opinion Words Extraction with Target-fused Neural Sequence Labeling. </span><em>Zhifang Fan, Zhen Wu, Xin-Yu Dai, Shujian Huang and Jiajun Chen</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers2" id="session-6b"><div id="expander"></div><a href="#" class="session-title">6B: Summarization</a><br/><span class="session-time" title="Tuesday, June 04, 2019">15:30 &ndash; 17:00</span><br/><span class="session-location btn btn--location">Greenway</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-6b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-6b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Ani Nenkova</td></tr>
<tr id="paper" paper-id="131"><td id="paper-time">15:30&ndash;15:48</td><td><span class="paper-title">Abstractive Summarization of Reddit Posts with Multi-level Memory Networks. </span><em>Byeongchang Kim, Hyunwoo Kim and Gunhee Kim</em></td></tr>
<tr id="paper" paper-id="767"><td id="paper-time">15:48&ndash;16:06</td><td><span class="paper-title">Automatic learner summary assessment for reading comprehension. </span><em>Menglin Xia, Ekaterina Kochmar and Ted Briscoe</em></td></tr>
<tr id="paper" paper-id="1416"><td id="paper-time">16:06&ndash;16:24</td><td><span class="paper-title">Data-efficient Neural Text Compression with Interactive Learning. </span><em>Avinesh P.V.S and Christian M. Meyer</em></td></tr>
<tr id="paper" paper-id="1829"><td id="paper-time">16:24&ndash;16:42</td><td><span class="paper-title">Text Generation with Exemplar-based Adaptive Decoding. </span><em>Hao Peng, Ankur Parikh, Manaal Faruqui, Bhuwan Dhingra and Dipanjan Das</em></td></tr>
<tr id="paper" paper-id="1914"><td id="paper-time">16:42&ndash;17:00</td><td><span class="paper-title">Guiding Extractive Summarization with Question-Answering Rewards. </span><em>Kristjan Arumae and Fei Liu</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers3" id="session-6c"><div id="expander"></div><a href="#" class="session-title">6C: Vision</a><br/><span class="session-time" title="Tuesday, June 04, 2019">15:30 &ndash; 17:00</span><br/><span class="session-location btn btn--location">Nicollet A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-6c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-6c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: William Yang Wang</td></tr>
<tr id="paper" paper-id="1058"><td id="paper-time">15:30&ndash;15:48</td><td><span class="paper-title">Beyond task success: A closer look at jointly learning to see, ask, and GuessWhat. </span><em>Ravi Shekhar, Aashish Venkatesh, Tim Baumgärtner, Elia Bruni, Barbara Plank, Raffaella Bernardi and Raquel Fernández</em></td></tr>
<tr id="paper" paper-id="1302"><td id="paper-time">15:48&ndash;16:06</td><td><span class="paper-title">The World in My Mind: Visual Dialog with Adversarial Multi-modal Feature Encoding. </span><em>Yiqun Yao, Jiaming Xu and Bo Xu</em></td></tr>
<tr id="paper" paper-id="1632"><td id="paper-time">16:06&ndash;16:24</td><td><span class="paper-title">Strong and Simple Baselines for Multimodal Utterance Embeddings. </span><em>Paul Pu Liang, Yao Chong Lim, Yao-Hung Hubert Tsai, Ruslan Salakhutdinov and Louis-Philippe Morency</em></td></tr>
<tr id="paper" paper-id="1636"><td id="paper-time">16:24&ndash;16:42</td><td><span class="paper-title">Learning to Navigate Unseen Environments: Back Translation with Environmental Dropout. </span><em>Hao Tan, Licheng Yu and Mohit Bansal</em></td></tr>
<tr id="paper" paper-id="1995"><td id="paper-time">16:42&ndash;17:00</td><td><span class="paper-title">Towards Content Transfer through Grounded Text Generation. </span><em>Shrimai Prabhumoye, Chris Quirk and Michel Galley</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers4" id="session-6d"><div id="expander"></div><a href="#" class="session-title">6D: Question Answering</a><br/><span class="session-time" title="Tuesday, June 04, 2019">15:30 &ndash; 17:00</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-6d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-6d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Eduardo Blanco</td></tr>
<tr id="paper" paper-id="103"><td id="paper-time">15:30&ndash;15:48</td><td><span class="paper-title">Improving Machine Reading Comprehension with General Reading Strategies. </span><em>Kai Sun, Dian Yu, Dong Yu and Claire Cardie</em></td></tr>
<tr id="paper" paper-id="772"><td id="paper-time">15:48&ndash;16:06</td><td><span class="paper-title">Multi-task Learning with Sample Re-weighting for Machine Reading Comprehension. </span><em>Yichong Xu, Xiaodong Liu, Yelong Shen, Jingjing Liu and Jianfeng Gao</em></td></tr>
<tr id="paper" paper-id="1001"><td id="paper-time">16:06&ndash;16:24</td><td><span class="paper-title">Semantically-Aligned Equation Generation for Solving and Reasoning Math Word Problems. </span><em>Ting-Rui Chiang and Yun-Nung Chen</em></td></tr>
<tr id="paper" paper-id="2080"><td id="paper-time">16:24&ndash;16:42</td><td><span class="paper-title">Iterative Search for Weakly Supervised Semantic Parsing. </span><em>Pradeep Dasigi, Matt Gardner, Shikhar Murty, Luke Zettlemoyer and Eduard Hovy</em></td></tr>
<tr id="paper" paper-id="1861"><td id="paper-time">16:42&ndash;17:00</td><td><span class="paper-title">Alignment over Heterogeneous Embeddings for Question Answering. </span><em>Vikas Yadav, Steven Bethard and Mihai Surdeanu</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers5" id="session-6e"><div id="expander"></div><a href="#" class="session-title">6E: Industry: Deployed Systems</a><br/><span class="session-time" title="Tuesday, June 04, 2019">15:30 &ndash; 17:00</span><br/><span class="session-location btn btn--location">Nicollet D</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-6e-selector"> Choose All</a><a href="#" class="session-deselector" id="session-6e-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Rashmi Gangadharaiah</td></tr>
<tr id="paper" paper-id="4023-industry"><td id="paper-time">15:30&ndash;15:48</td><td><span class="paper-title">Diversifying Reply Suggestions Using a Matching-Conditional Variational Autoencoder. </span><em>Budhaditya Deb, Peter Bailey and Milad Shokouhi</em></td></tr>
<tr id="paper" paper-id="4031-industry"><td id="paper-time">15:48&ndash;16:06</td><td><span class="paper-title">Goal-Oriented End-to-End Conversational Models with Profile Features in a Real-World Setting. </span><em>Yichao Lu, Manisha Srivastava, Jared Kramer, Heba Elfardy, Andrea Kahn, Song Wang and Vikas Bhardwaj</em></td></tr>
<tr id="paper" paper-id="4052-industry"><td id="paper-time">16:06&ndash;16:24</td><td><span class="paper-title">Detecting Customer Complaint Escalation with Recurrent Neural Networks and Manually-Engineered Features. </span><em>Wei Yang, Luchen Tan, Chunwei Lu, Anqi Cui, Han Li, Xi Chen, Kun Xiong, Muzi Wang, Ming Li, Jian Pei and Jimmy Lin</em></td></tr>
<tr id="paper" paper-id="4098-industry"><td id="paper-time">16:24&ndash;16:42</td><td><span class="paper-title">Multi-Modal Generative Adversarial Network for Short Product Title Generation in Mobile E-Commerce. </span><em>Jianguo Zhang, Pengcheng Zou, Zhao Li, Yao Wan, Xiuming Pan, Yu Gong and Philip S. Yu</em></td></tr>
<tr id="paper" paper-id="4120-industry"><td id="paper-time">16:42&ndash;17:00</td><td><span class="paper-title">A Case Study on Neural Headline Generation for Editing Support. </span><em>Kazuma Murao, Ken Kobayashi, Hayato Kobayashi, Taichi Yatsuka, Takeshi Masuyama, Tatsuru Higurashi and Yoshimune Tabuchi</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-posters" id="session-poster-6"><div id="expander"></div><a href="#" class="session-title">6F: Phonology & Morphology, Speech and Text Mining (Posters & Demos) </a><br/><span class="session-time" title="Tuesday, June 04, 2019">15:30 &ndash; 17:00</span><br/><span class="session-location btn btn--location">Hyatt Exhibit Hall</span><div class="poster-session-details"><br/><table class="poster-table">
<tr><td><span class="poster-type">Phonology & Morphology</span></td></tr>
<tr id="poster" poster-id="201"><td><span class="poster-title">Bridging the Gap: Attending to Discontinuity in Identification of Multiword Expressions. </span><em>Omid Rohanian, Shiva Taslimipoor, Samaneh Kouchaki, Le An Ha and Ruslan Mitkov</em></td></tr>
<tr id="poster" poster-id="265"><td><span class="poster-title">Incorporating Word Attention into Character-Based Word Segmentation. </span><em>Shohei Higashiyama, Masao Utiyama, Eiichiro Sumita, Masao Ideuchi, Yoshiaki Oida, Yohei Sakamoto and Isaac Okada</em></td></tr>
<tr id="poster" poster-id="448"><td><span class="poster-title">VCWE: Visual Character-Enhanced Word Embeddings. </span><em>Chi Sun, Xipeng Qiu and Xuanjing Huang</em></td></tr>
<tr id="poster" poster-id="657"><td><span class="poster-title">Subword Encoding in Lattice LSTM for Chinese Word Segmentation. </span><em>Jie Yang, Yue Zhang and Shuailong Liang</em></td></tr>
<tr id="poster" poster-id="973"><td><span class="poster-title">Improving Cross-Domain Chinese Word Segmentation with Word Embeddings. </span><em>Yuxiao Ye, Weikang Li, Yue Zhang, Likun Qiu and Jian Sun</em></td></tr>
<tr id="poster" poster-id="997"><td><span class="poster-title">Neural Semi-Markov Conditional Random Fields for Robust Character-Based Part-of-Speech Tagging. </span><em>Apostolos Kemos, Heike Adel and Hinrich Schütze</em></td></tr>
<tr id="poster" poster-id="1193"><td><span class="poster-title">Shrinking Japanese Morphological Analyzers With Neural Networks and Semi-supervised Learning. </span><em>Arseny Tolmachev, Daisuke Kawahara and Sadao Kurohashi</em></td></tr>
<tr id="poster" poster-id="2485-tacl"><td><span class="poster-title">Grammar Error Correction in Morphologically-Rich Languages: The Case of Russian. </span><em>Alla Rozovskaya and Dan Roth</em></td></tr>
<tr id="poster" poster-id="49-srw"><td><span class="poster-title">Deep Learning and Sociophonetics: Automatic Coding of Rhoticity Using Neural Networks. </span><em>Sarah Gupta and Anthony DiPadova</em></td></tr>
<tr id="poster" poster-id="60-srw"><td><span class="poster-title">Learn Languages First and Then Convert: towards Effective Simplified to Traditional Chinese Conversion. </span><em>Pranav A, S.F. Hui, I-Tsun Cheng, Ishaan Batra and Chiu Yik Hei</em></td></tr>
<tr><td><span class="poster-type">Speech</span></td></tr>
<tr id="poster" poster-id="541"><td><span class="poster-title">Neural Constituency Parsing of Speech Transcripts. </span><em>Paria Jamshid Lou, Yufei Wang and Mark Johnson</em></td></tr>
<tr id="poster" poster-id="1783"><td><span class="poster-title">Acoustic-to-Word Models with Conversational Context Information. </span><em>Suyoun Kim and Florian Metze</em></td></tr>
<tr id="poster" poster-id="1848"><td><span class="poster-title">A Dynamic Speaker Model for Conversational Interactions. </span><em>Hao Cheng, Hao Fang and Mari Ostendorf</em></td></tr>
<tr id="poster" poster-id="2263"><td><span class="poster-title">Fluent Translations from Disfluent Speech in End-to-End Speech Translation. </span><em>Elizabeth Salesky, Matthias Sperber and Alexander Waibel</em></td></tr>
<tr id="poster" poster-id="35-srw"><td><span class="poster-title">Data Augmentation by Data Noising for Open-vocabulary Slots in Spoken Language Understanding. </span><em>Hwa-Yeon Kim, Yoon-Hyung Roh and Young-Kil Kim</em></td></tr>
<tr id="poster" poster-id="59-srw"><td><span class="poster-title">Expectation and Locality Effects in the Prediction of Disfluent Fillers and Repairs in English Speech. </span><em>Samvit Dammalapati, Rajakrishnan Rajkumar and Sumeet Agarwal</em></td></tr>
<tr><td><span class="poster-type">Text Mining</span></td></tr>
<tr id="poster" poster-id="197"><td><span class="poster-title">Relation Classification Using Segment-Level Attention-based CNN and Dependency-based RNN. </span><em>Van-Hien Tran, Van-Thuy Phi, Hiroyuki Shindo and Yuji Matsumoto</em></td></tr>
<tr id="poster" poster-id="261"><td><span class="poster-title">Document-Level Event Factuality Identification via Adversarial Neural Network. </span><em>Zhong Qian, Peifeng Li, Qiaoming Zhu and Guodong Zhou</em></td></tr>
<tr id="poster" poster-id="423"><td><span class="poster-title">Distant Supervision Relation Extraction with Intra-Bag and Inter-Bag Attentions. </span><em>Zhi-Xiu Ye and Zhen-Hua Ling</em></td></tr>
<tr id="poster" poster-id="750"><td><span class="poster-title">Ranking-Based Autoencoder for Extreme Multi-label Classification. </span><em>Bingyu Wang, Li Chen, Wei Sun, Kechen Qin, Kefeng Li and Hui Zhou</em></td></tr>
<tr id="poster" poster-id="901"><td><span class="poster-title">Posterior-regularized REINFORCE for Instance Selection in Distant Supervision. </span><em>Qi Zhang, Siliang Tang, Xiang Ren, Fei Wu, Shiliang Pu and Yueting Zhuang</em></td></tr>
<tr id="poster" poster-id="968"><td><span class="poster-title">Scalable Collapsed Inference for High-Dimensional Topic Models. </span><em>Rashidul Islam and James Foulds</em></td></tr>
<tr id="poster" poster-id="1164"><td><span class="poster-title">An Integrated Approach for Keyphrase Generation via Exploring the Power of Retrieval and Extraction. </span><em>Wang Chen, Hou Pong Chan, Piji Li, Lidong Bing and Irwin King</em></td></tr>
<tr id="poster" poster-id="1474"><td><span class="poster-title">Predicting Malware Attributes from Cybersecurity Texts. </span><em>Arpita Roy, Youngja Park and Shimei Pan</em></td></tr>
<tr id="poster" poster-id="1590"><td><span class="poster-title">Improving Distantly-supervised Entity Typing with Compact Latent Space Clustering. </span><em>Bo Chen, Xiaotao Gu, Yufeng Hu, Siliang Tang, Guoping Hu, Yueting Zhuang and Xiang Ren</em></td></tr>
<tr id="poster" poster-id="1852"><td><span class="poster-title">Modelling Instance-Level Annotator Reliability for Natural Language Labelling Tasks. </span><em>Maolin Li, Arvid Fahlström Myrman, Tingting Mu and Sophia Ananiadou</em></td></tr>
<tr id="poster" poster-id="2082"><td><span class="poster-title">Review-Driven Multi-Label Music Style Classification by Exploiting Style Correlations. </span><em>Guangxiang Zhao, Jingjing Xu, Qi Zeng, Xuancheng Ren and Xu Sun</em></td></tr>
<tr id="poster" poster-id="2219"><td><span class="poster-title">Fact Discovery from Knowledge Base via Facet Decomposition. </span><em>Zihao Fu, Yankai Lin, Zhiyuan Liu and Wai Lam</em></td></tr>
<tr id="poster" poster-id="2429"><td><span class="poster-title">A Richer-but-Smarter Shortest Dependency Path with Attentive Augmentation for Relation Extraction. </span><em>Duy-Cat Can, Hoang-Quynh Le, Quang-Thuy Ha and Nigel Collier</em></td></tr>
<tr id="poster" poster-id="6-demos"><td><span class="poster-title">Multilingual Entity, Relation, Event and Human Value Extraction. </span><em>Manling Li, Ying Lin, Joseph Hoover, Spencer Whitehead, Clare Voss, Morteza Dehghani and Heng Ji</em></td></tr>
<tr id="poster" poster-id="43-demos"><td><span class="poster-title">Litigation Analytics: Extracting and querying motions and orders from US federal courts. </span><em>Thomas Vacek, Dezhao Song, Hugo Molina-Salgado, Ronald Teo, Conner Cowling and Frank Schilder</em></td></tr>
<tr id="poster" poster-id="50-demos"><td><span class="poster-title">Community lexical access for an endangered polysynthetic language: An electronic dictionary for St. Lawrence Island Yupik. </span><em>Benjamin Hunt, Emily Chen, Sylvia L.R. Schreiner and Lane Schwartz</em></td></tr>
<tr id="poster" poster-id="42-demos"><td><span class="poster-title">Visualizing Inferred Morphotactic Systems. </span><em>Haley Lepp, Olga Zamaraeva and Emily M. Bender</em></td></tr>
<tr id="poster" poster-id="40-demos"><td><span class="poster-title">A Research Platform for Multi-Robot Dialogue with Humans. </span><em>Matthew Marge, Stephen Nogar, Cory J. Hayes, Stephanie M. Lukin, Jesse Bloecker, Eric Holder and Clare Voss</em></td></tr>
<tr id="poster" poster-id="13-demos"><td><span class="poster-title">Chat-crowd: A Dialog-based Platform for Visual Layout Composition. </span><em>Paola Cascante-Bonilla, Xuwang Yin, Vicente Ordonez and Song Feng</em></td></tr>
</table>
</div>
</div>
</div>
<div class="session session-plenary"><span class="session-title">Social Event</span><br/><span class="session-time" title="Tuesday, June 04, 2019">19:00 &ndash; 22:00</span><br/><span class="session-external-location btn btn--location">Minneapolis Institute of Art </span></div>
<div class="day" id="day-4">Wednesday, June 05, 2019</div>
<div class="session session-expandable session-plenary"><div id="expander"></div><a href="#" class="session-title"><strong>Keynote 3: Kieran Snyder "Leaving the Lab: Building NLP Applications that Real People can Use"</strong></a><br/><span class="session-person"><a href="https://textio.com/team/" target="_blank">Kieran Snyder</a></span><br/><span class="session-time" title="Wednesday, June 05, 2019">9:00 &ndash; 10:00</span><br/><span class="session-location btn btn--location">Nicollet Grand Ballroom</span><div class="paper-session-details"><br/><div class="session-abstract"><p>There is a chasm between an NLP technology that works well in the research lab and something that works for applications that real people use. Research conditions are often theoretical or idealized. The first time they contribute to industry projects, many theoretical researchers are surprised to discover how much goes into building outside the lab, and how hard it is to build data products for real people ethically and transparently. This talk explores my NLP journey in three stages: working as an academic NLP researcher, learning to be a practical creator of NLP products in industry, and becoming the founding CEO of an NLP business. While each role has used my background in computational linguistics in essential ways, every step has also required me to learn and unlearn new things along the way. The further I have gone in my industry career, the more critical it has become to define and work within a well-established set of principles for data ethics. This talk is for academic researchers considering industry careers or collaborations, for people in industry who started out in academia, and for anyone on either side of the divide who wants to make NLP products that real people can use.</p></div></div></div>
<div class="session session-break session-plenary" id="session-break-12"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Wednesday, June 05, 2019">10:00 &ndash; 10:30</span></div>
<div class="session-box" id="session-box-7">
<div class="session-header" id="session-header-7">Long Orals / Long & Short Posters</div>
<div class="session session-expandable session-papers1" id="session-7a"><div id="expander"></div><a href="#" class="session-title">7A: Question Answering</a><br/><span class="session-time" title="Wednesday, June 05, 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--location">Greenway</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-7a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-7a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Alessandro Moschitti</td></tr>
<tr id="paper" paper-id="734"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Bidirectional Attentive Memory Networks for Question Answering over Knowledge Bases. </span><em>Yu Chen, Lingfei Wu and Mohammed J Zaki</em></td></tr>
<tr id="paper" paper-id="1626"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions. </span><em>Christopher Clark, Kenton Lee, Ming-Wei Chang, Tom Kwiatkowski, Michael Collins and Kristina Toutanova</em></td></tr>
<tr id="paper" paper-id="1770"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Enhancing Key-Value Memory Neural Networks for Knowledge Based Question Answering. </span><em>Kun Xu, Yuxuan Lai, Yansong Feng and Zhiguo Wang</em></td></tr>
<tr id="paper" paper-id="2300"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Repurposing Entailment for Multi-Hop Question Answering Tasks. </span><em>Harsh Trivedi, Heeyoung Kwon, Tushar Khot, Ashish Sabharwal and Niranjan Balasubramanian</em></td></tr>
<tr id="paper" paper-id="2480-tacl"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">CoQA: A Conversational Question Answering Challenge. </span><em>Siva Reddy, Danqi Chen and Christopher D. Manning</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers2" id="session-7b"><div id="expander"></div><a href="#" class="session-title">7B: Ethics, Bias & Fairness</a><br/><span class="session-time" title="Wednesday, June 05, 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--location">Nicollet A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-7b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-7b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Emily Prud'hommeaux</td></tr>
<tr id="paper" paper-id="2479-tacl"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Mind the GAP: A Balanced Corpus of Gendered Ambiguous Pronouns. </span><em>Kellie Webster, Marta Recasens, Vera Axelrod and Jason Baldridge</em></td></tr>
<tr id="paper" paper-id="2087"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">GenderQuant: Quantifying Mention-Level Genderedness. </span><em> Ananya, Nitya Parthasarthi and Sameer Singh</em></td></tr>
<tr id="paper" paper-id="2238"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Analyzing Polarization in Social Media: Method and Application to Tweets on 21 Mass Shootings. </span><em>Dorottya Demszky, Nikhil Garg, Rob Voigt, James Zou, Jesse Shapiro, Matthew Gentzkow and Dan Jurafsky</em></td></tr>
<tr id="paper" paper-id="1396"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Learning to Decipher Hate Symbols. </span><em>Jing Qian, Mai ElSherief, Elizabeth Belding and William Yang Wang</em></td></tr>
<tr id="paper" paper-id="2482-tacl"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Data Statements for Natural Language Processing: Toward Mitigating System Bias and Enabling Better Science. </span><em>Emily M. Bender and Batya Friedman</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers3" id="session-7c"><div id="expander"></div><a href="#" class="session-title">7C: Information Extraction</a><br/><span class="session-time" title="Wednesday, June 05, 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--location">Nicollet D</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-7c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-7c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Heng Ji</td></tr>
<tr id="paper" paper-id="147"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Long-tail Relation Extraction via Knowledge Graph Embeddings and Graph Convolution Networks. </span><em>Ningyu Zhang, Shumin Deng, Zhanlin Sun, Guanying Wang, Xi Chen, Wei Zhang and Huajun Chen</em></td></tr>
<tr id="paper" paper-id="439"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">GAN Driven Semi-distant Supervision for Relation Extraction. </span><em>Pengshuai Li, Xinsong Zhang, Weijia Jia and Hai Zhao</em></td></tr>
<tr id="paper" paper-id="1011"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">A general framework for information extraction using dynamic span graphs. </span><em>Yi Luan, Dave Wadden, Luheng He, Amy Shah, Mari Ostendorf and Hannaneh Hajishirzi</em></td></tr>
<tr id="paper" paper-id="1374"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">OpenCeres: When Open Information Extraction Meets the Semi-Structured Web. </span><em>Colin Lockard, Prashant Shiralkar and Xin Luna Dong</em></td></tr>
<tr id="paper" paper-id="1447"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Structured Minimally Supervised Learning for Neural Relation Extraction. </span><em>Fan Bai and Alan Ritter</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers4" id="session-7d"><div id="expander"></div><a href="#" class="session-title">7D: Machine Translation</a><br/><span class="session-time" title="Wednesday, June 05, 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--location">Northstar A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-7d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-7d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Colin Cherry</td></tr>
<tr id="paper" paper-id="896"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Neural Machine Translation of Text from Non-Native Speakers. </span><em>Antonios Anastasopoulos, Alison Lui, Toan Q. Nguyen and David Chiang</em></td></tr>
<tr id="paper" paper-id="1183"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Improving Domain Adaptation Translation with Domain Invariant and Specific Information. </span><em>Shuhao Gu, Yang Feng and Qun Liu</em></td></tr>
<tr id="paper" paper-id="1819"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Selective Attention for Context-aware Neural Machine Translation. </span><em>Sameen Maruf, André F. T. Martins and Gholamreza Haffari</em></td></tr>
<tr id="paper" paper-id="2018"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">On Evaluation of Adversarial Perturbations for Sequence-to-Sequence Models. </span><em>Paul Michel, Xian Li, Graham Neubig and Juan Pino</em></td></tr>
<tr id="paper" paper-id="2242"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Accelerated Reinforcement Learning for Sentence Generation by Vocabulary Prediction. </span><em>Kazuma Hashimoto and Yoshimasa Tsuruoka</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers5" id="session-7e"><div id="expander"></div><a href="#" class="session-title">7E: Text Analysis</a><br/><span class="session-time" title="Wednesday, June 05, 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-7e-selector"> Choose All</a><a href="#" class="session-deselector" id="session-7e-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Steven Bethard</td></tr>
<tr id="paper" paper-id="2159"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Mitigating Uncertainty in Document Classification. </span><em>Xuchao Zhang, Fanglan Chen, ChangTien Lu and Naren Ramakrishnan</em></td></tr>
<tr id="paper" paper-id="1455"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Complexity-Weighted Loss and Diverse Reranking for Sentence Simplification. </span><em>Reno Kriz, Joao Sedoc, Marianna Apidianaki, Carolina Zheng, Gaurav Kumar, Eleni Miltsakaki and Chris Callison-Burch</em></td></tr>
<tr id="paper" paper-id="1533"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Predicting Helpful Posts in Open-Ended Discussion Forums: A Neural Architecture. </span><em>Kishaloy Halder, Min-Yen Kan and Kazunari Sugiyama</em></td></tr>
<tr id="paper" paper-id="1994"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Text Classification with Few Examples using Controlled Generalization. </span><em>Abhijit Mahabal, Jason Baldridge, Burcu Karagol Ayan, Vincent Perot and Dan Roth</em></td></tr>
<tr id="paper" paper-id="236"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Reinforcement Learning Based Text Style Transfer without Parallel Training Corpus. </span><em>Hongyu Gong, Suma Bhat, Lingfei Wu, JinJun Xiong and Wen-mei Hwu</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-posters" id="session-poster-7"><div id="expander"></div><a href="#" class="session-title">7F: Machine Learning, Tagging, Chunking, Syntax  & Parsing  (Posters) </a><br/><span class="session-time" title="Wednesday, June 05, 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--location">Hyatt Exhibit Hall</span><div class="poster-session-details"><br/><table class="poster-table">
<tr><td><span class="poster-type">Machine Learning</span></td></tr>
<tr id="poster" poster-id="252"><td><span class="poster-title">Adapting RNN Sequence Prediction Model to Multi-label Set Prediction. </span><em>Kechen Qin, Cheng Li, Virgil Pavlu and Javed Aslam</em></td></tr>
<tr id="poster" poster-id="481"><td><span class="poster-title">Customizing Grapheme-to-Phoneme System for Non-Trivial Transcription Problems in Bangla Language. </span><em>Sudipta Saha Shubha, Nafis Sadeq, Shafayat Ahmed, Md. Nahidul Islam, Muhammad Abdullah Adnan, Md. Yasin Ali Khan and Mohammad Zuberul Islam</em></td></tr>
<tr id="poster" poster-id="497"><td><span class="poster-title">Connecting Language and Knowledge with Heterogeneous Representations for Neural Relation Extraction. </span><em>Peng Xu and Denilson Barbosa</em></td></tr>
<tr id="poster" poster-id="773"><td><span class="poster-title">Segmentation-free compositional n-gram embedding. </span><em>Geewook Kim, Kazuki Fukui and Hidetoshi Shimodaira</em></td></tr>
<tr id="poster" poster-id="1117"><td><span class="poster-title">Exploiting Noisy Data in Distant Supervision Relation Classification. </span><em>Kaijia Yang, Liang He, Xin-Yu Dai, Shujian Huang and Jiajun Chen</em></td></tr>
<tr id="poster" poster-id="1348"><td><span class="poster-title">Misspelling Oblivious Word Embeddings. </span><em>Aleksandra Piktus, Necati Bora Edizel, Piotr Bojanowski, Edouard Grave, Rui Ferreira and Fabrizio Silvestri</em></td></tr>
<tr id="poster" poster-id="1357"><td><span class="poster-title">Learning Relational Representations by Analogy using Hierarchical Siamese Networks. </span><em>Gaetano Rossiello, Alfio Gliozzo, Robert Farrell, Nicolas Fauceglia and Michael Glass</em></td></tr>
<tr id="poster" poster-id="1375"><td><span class="poster-title">An Effective Label Noise Model for DNN Text Classification. </span><em>Ishan Jindal, Daniel Pressel, Brian Lester and Matthew Nokleby</em></td></tr>
<tr id="poster" poster-id="1402"><td><span class="poster-title">Understanding Learning Dynamics Of Language Models with SVCCA. </span><em>Naomi Saphra and Adam Lopez</em></td></tr>
<tr id="poster" poster-id="1441"><td><span class="poster-title">Using Large Corpus N-gram Statistics to Improve Recurrent Neural Language Models. </span><em>Yiben Yang, Ji-Ping Wang and Doug Downey</em></td></tr>
<tr id="poster" poster-id="1555"><td><span class="poster-title">Continual Learning for Sentence Representations Using Conceptors. </span><em>Tianlin Liu, Lyle Ungar and Joao Sedoc</em></td></tr>
<tr id="poster" poster-id="1563"><td><span class="poster-title">Relation Discovery with Out-of-Relation Knowledge Base as Supervision. </span><em>Yan Liang, Xin Liu, Jianwen Zhang and Yangqiu Song</em></td></tr>
<tr id="poster" poster-id="1742"><td><span class="poster-title">Corpora Generation for Grammatical Error Correction. </span><em>Jared Lichtarge, Chris Alberti, Shankar Kumar, Noam Shazeer, Niki Parmar and Simon Tong</em></td></tr>
<tr id="poster" poster-id="1841"><td><span class="poster-title">Structural Supervision Improves Learning of Non-Local Grammatical Dependencies. </span><em>Ethan Wilcox, Peng Qian, Richard Futrell, Miguel Ballesteros and Roger Levy</em></td></tr>
<tr id="poster" poster-id="1932"><td><span class="poster-title">Benchmarking Approximate Inference Methods for Neural Structured Prediction. </span><em>Lifu Tu and Kevin Gimpel</em></td></tr>
<tr id="poster" poster-id="1942"><td><span class="poster-title">Evaluating and Enhancing the Robustness of Dialogue Systems: A Case Study on a Negotiation Agent. </span><em>Minhao Cheng, Wei Wei and Cho-Jui Hsieh</em></td></tr>
<tr id="poster" poster-id="2020"><td><span class="poster-title">Investigating Robustness and Interpretability of Link Prediction via Adversarial Modifications. </span><em>Pouya Pezeshkpour, Yifan Tian and Sameer Singh</em></td></tr>
<tr id="poster" poster-id="2478-tacl"><td><span class="poster-title">Analysis Methods in Neural Language Processing: A Survey. </span><em>Yonatan Belinkov and James Glass</em></td></tr>
<tr id="poster" poster-id="2481-tacl"><td><span class="poster-title">Attentive Convolution: Equipping CNNs with RNN-style Attention Mechanisms. </span><em>Wenpeng Yin and Hinrich Schütze</em></td></tr>
<tr id="poster" poster-id="2486-tacl"><td><span class="poster-title">Rotational Unit of Memory: A Novel Representation Unit for RNNs with Scalable Applications. </span><em>Rumen Dangovski, Li Jing, Preslav Nakov, Mićo Tatalović and Marin Soljačić</em></td></tr>
<tr id="poster" poster-id="1851"><td><span class="poster-title">Transferable Neural Projection Representations. </span><em>Chinnadhurai Sankar, Sujith Ravi and Zornitsa Kozareva</em></td></tr>
<tr id="poster" poster-id="34-srw"><td><span class="poster-title">Gating Mechanisms for Combining Character and Word-level Word Representations: an Empirical Study. </span><em>Jorge Balazs and Yutaka Matsuo</em></td></tr>
<tr><td><span class="poster-type">Tagging, Chunking, Syntax  & Parsing</span></td></tr>
<tr id="poster" poster-id="443"><td><span class="poster-title">Semantic Role Labeling with Associated Memory Network. </span><em>Chaoyu Guan, Yuhao Cheng and Hai Zhao</em></td></tr>
<tr id="poster" poster-id="596"><td><span class="poster-title">Better, Faster, Stronger Sequence Tagging Constituent Parsers. </span><em>David Vilares, Mostafa Abdou and Anders Søgaard</em></td></tr>
<tr id="poster" poster-id="685"><td><span class="poster-title">CAN-NER: Convolutional Attention Network for Chinese Named Entity Recognition. </span><em>Yuying Zhu and Guoxin Wang</em></td></tr>
<tr id="poster" poster-id="863"><td><span class="poster-title">Decomposed Local Models for Coordinate Structure Parsing. </span><em>Hiroki Teranishi, Hiroyuki Shindo and Yuji Matsumoto</em></td></tr>
<tr id="poster" poster-id="943"><td><span class="poster-title">Multi-Task Learning for Japanese Predicate Argument Structure Analysis. </span><em>Hikaru Omori and Mamoru Komachi</em></td></tr>
<tr id="poster" poster-id="1107"><td><span class="poster-title">Domain adaptation for part-of-speech tagging of noisy user-generated text. </span><em>Luisa März, Dietrich Trautmann and Benjamin Roth</em></td></tr>
<tr id="poster" poster-id="1281"><td><span class="poster-title">Neural Chinese Address Parsing. </span><em>Hao Li, Wei Lu, Pengjun Xie and Linlin Li</em></td></tr>
<tr id="poster" poster-id="17-srw"><td><span class="poster-title">A Pregroup Representation of Word Order Alternation Using Hindi Syntax. </span><em>Alok Debnath and Manish Shrivastava</em></td></tr>
</table>
</div>
</div>
</div>
<div class="session session-break session-plenary" id="session-break-13"><span class="session-title">Grab your lunch break</span><br/><span class="session-time" title="Wednesday, June 05, 2019">12:00 &ndash; 12:30</span></div>
<div class="session session-expandable session-plenary"><div id="expander"></div><a href="#" class="session-title"><strong>NAACL Business Meeting</strong></a><br/><span class="session-time" title="Wednesday, June 05, 2019">12:30 &ndash; 13:30</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><div class="paper-session-details"><br/><div class="session-abstract"><p>All attendees are encouraged to participate in the business meeting.</p></div></div></div>
<div class="session-box" id="session-box-8">
<div class="session-header" id="session-header-8">Long Orals / Long & Short Posters</div>
<div class="session session-expandable session-papers1" id="session-8a"><div id="expander"></div><a href="#" class="session-title">8A: Discourse</a><br/><span class="session-time" title="Wednesday, June 05, 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--location">Northstar A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-8a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-8a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Vincent Ng</td></tr>
<tr id="paper" paper-id="145"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Learning Hierarchical Discourse-level Structure for Fake News Detection. </span><em>Hamid Karimi and Jiliang Tang</em></td></tr>
<tr id="paper" paper-id="732"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">DiscoFuse: A Large-Scale Dataset for Discourse-Based Sentence Fusion. </span><em>Mor Geva, Eric Malmi, Idan Szpektor and Jonathan Berant</em></td></tr>
<tr id="paper" paper-id="915"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Linguistically-Informed Specificity and Semantic Plausibility for Dialogue Generation. </span><em>Wei-Jen Ko, Greg Durrett and Junyi Jessy Li</em></td></tr>
<tr id="paper" paper-id="935"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Learning to Describe Unknown Phrases with Local and Global Contexts. </span><em>Shonosuke Ishiwatari, Hiroaki Hayashi, Naoki Yoshinaga, Graham Neubig, Shoetsu Sato, Masashi Toyoda and Masaru Kitsuregawa</em></td></tr>
<tr id="paper" paper-id="2327"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Mining Discourse Markers for Unsupervised Sentence Representation Learning. </span><em>Damien Sileo, Tim Van de Cruys, Camille Pradel and Philippe Muller</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers2" id="session-8b"><div id="expander"></div><a href="#" class="session-title">8B: Machine Learning</a><br/><span class="session-time" title="Wednesday, June 05, 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-8b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-8b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Anna Rumshisky</td></tr>
<tr id="paper" paper-id="238"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">How Large a Vocabulary Does Text Classification Need? A Variational Approach to Vocabulary Selection. </span><em>Wenhu Chen, Yu Su, Yilin Shen, Zhiyu Chen, Xifeng Yan and William Yang Wang</em></td></tr>
<tr id="paper" paper-id="931"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Subword-based Compact Reconstruction of Word Embeddings. </span><em>Shota Sasaki, Jun Suzuki and Kentaro Inui</em></td></tr>
<tr id="paper" paper-id="1059"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Bayesian Learning for Neural Dependency Parsing. </span><em>Ehsan Shareghi, Yingzhen Li, Yi Zhu, Roi Reichart and Anna Korhonen</em></td></tr>
<tr id="paper" paper-id="1506"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">AutoSeM: Automatic Task Selection and Mixing in Multi-Task Learning. </span><em>Han Guo, Ramakanth Pasunuru and Mohit Bansal</em></td></tr>
<tr id="paper" paper-id="1562"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Studying the Inductive Biases of RNNs with Synthetic Variations of Natural Languages. </span><em>Shauli Ravfogel, Yoav Goldberg and Tal Linzen</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers3" id="session-8c"><div id="expander"></div><a href="#" class="session-title">8C: Applications</a><br/><span class="session-time" title="Wednesday, June 05, 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--location">Nicollet A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-8c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-8c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: T. J. Hazen</td></tr>
<tr id="paper" paper-id="297"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Attention is not Explanation. </span><em>Sarthak Jain and Byron C. Wallace</em></td></tr>
<tr id="paper" paper-id="724"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Playing Text-Adventure Games with Graph-Based Deep Reinforcement Learning. </span><em>Prithviraj Ammanabrolu and Mark Riedl</em></td></tr>
<tr id="paper" paper-id="1170"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Information Aggregation for Multi-Head Attention with Routing-by-Agreement. </span><em>Jian Li, Baosong Yang, Zi-Yi Dou, Xing Wang, Michael R. Lyu and Zhaopeng Tu</em></td></tr>
<tr id="paper" paper-id="1806"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Context Dependent Semantic Parsing over Temporally Structured Data. </span><em>Charles Chen and Razvan Bunescu</em></td></tr>
<tr id="paper" paper-id="2017"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Structural Scaffolds for Citation Intent Classification in Scientific Publications. </span><em>Arman Cohan, Waleed Ammar, Madeleine van Zuylen and Field Cady</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers4" id="session-8d"><div id="expander"></div><a href="#" class="session-title">8D: Semantics</a><br/><span class="session-time" title="Wednesday, June 05, 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--location">Greenway</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-8d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-8d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Matt Gardner</td></tr>
<tr id="paper" paper-id="766"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">pair2vec: Compositional Word-Pair Embeddings for Cross-Sentence Inference. </span><em>Mandar Joshi, Eunsol Choi, Omer Levy, Daniel Weld and Luke Zettlemoyer</em></td></tr>
<tr id="paper" paper-id="1285"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Submodular Optimization-based Diverse Paraphrasing and its Effectiveness in Data Augmentation. </span><em>Ashutosh Kumar, Satwik Bhattamishra, Manik Bhandari and Partha Talukdar</em></td></tr>
<tr id="paper" paper-id="1779"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Let’s Make Your Request More Persuasive: Modeling Persuasive Strategies via Semi-Supervised Neural Nets on Crowdfunding Platforms. </span><em>Diyi Yang, Jiaao Chen, Zichao Yang, Dan Jurafsky and Eduard Hovy</em></td></tr>
<tr id="paper" paper-id="1946"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Recursive Routing Networks: Learning to Compose Modules for Language Understanding. </span><em>Ignacio Cases, Clemens Rosenbaum, Matthew Riemer, Atticus Geiger, Tim Klinger, Alex Tamkin, Olivia Li, Sandhini Agarwal, Joshua D. Greene, Dan Jurafsky, Christopher Potts and Lauri Karttunen</em></td></tr>
<tr id="paper" paper-id="1086"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Structural Neural Encoders for AMR-to-text Generation. </span><em>Marco Damonte and Shay B. Cohen</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers5" id="session-8e"><div id="expander"></div><a href="#" class="session-title">8E: Bio & Clinical</a><br/><span class="session-time" title="Wednesday, June 05, 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--location">Nicollet D</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-8e-selector"> Choose All</a><a href="#" class="session-deselector" id="session-8e-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Timothy Miller</td></tr>
<tr id="paper" paper-id="725"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Multilingual prediction of Alzheimer’s disease through domain adaptation and concept-based language modelling. </span><em>Kathleen C. Fraser, Nicklas Linz, Bai Li, Kristina Lundholm Fors, Frank Rudzicz, Alexandra Konig, Jan Alexandersson, Philippe Robert and Dimitrios Kokkinakis</em></td></tr>
<tr id="paper" paper-id="797"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Ranking and Selecting Multi-Hop Knowledge Paths to Better Predict Human Needs. </span><em>Debjit Paul and Anette Frank</em></td></tr>
<tr id="paper" paper-id="1244"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">NLP Whack-A-Mole: Challenges in Cross-Domain Temporal Expression Extraction. </span><em>Amy Olex, Luke Maffey and Bridget McInnes</em></td></tr>
<tr id="paper" paper-id="1698"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Document-Level N-ary Relation Extraction with Multiscale Representation Learning. </span><em>Robin Jia, Cliff Wong and Hoifung Poon</em></td></tr>
<tr id="paper" paper-id="1825"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Inferring Which Medical Treatments Work from Reports of Clinical Trials. </span><em>Eric Lehman, Jay DeYoung, Regina Barzilay and Byron C. Wallace</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-posters" id="session-poster-8"><div id="expander"></div><a href="#" class="session-title">8F: Dialogue, Multilingual NLP & Summarization (Posters) </a><br/><span class="session-time" title="Wednesday, June 05, 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--location">Hyatt Exhibit Hall</span><div class="poster-session-details"><br/><table class="poster-table">
<tr><td><span class="poster-type">Dialogue</span></td></tr>
<tr id="poster" poster-id="191"><td><span class="poster-title">Decay-Function-Free Time-Aware Attention to Context and Speaker Indicator for Spoken Language Understanding. </span><em>Jonggu Kim and Jong-Hyeok Lee</em></td></tr>
<tr id="poster" poster-id="387"><td><span class="poster-title">Dialogue Act Classification with Context-Aware Self-Attention. </span><em>Vipul Raheja and Joel Tetreault</em></td></tr>
<tr id="poster" poster-id="389"><td><span class="poster-title">Affect-Driven Dialog Generation. </span><em>Pierre Colombo, Wojciech Witon, Ashutosh Modi, James Kennedy and Mubbasir Kapadia</em></td></tr>
<tr id="poster" poster-id="993"><td><span class="poster-title">Multi-Level Memory for Task Oriented Dialogs. </span><em>Revanth Gangi Reddy, Danish Contractor, Dinesh Raghu and Sachindra Joshi</em></td></tr>
<tr id="poster" poster-id="1223"><td><span class="poster-title">Topic Spotting using Hierarchical Networks with Self Attention. </span><em>Pooja Chitkara, Ashutosh Modi, Pravalika Avvaru, Sepehr Janghorbani and Mubbasir Kapadia</em></td></tr>
<tr id="poster" poster-id="1575"><td><span class="poster-title">Top-Down Structurally-Constrained Neural Response Generation with Lexicalized Probabilistic Context-Free Grammar. </span><em>Wenchao Du and Alan W. Black</em></td></tr>
<tr id="poster" poster-id="1724"><td><span class="poster-title">What do Entity-Centric Models Learn? Insights from Entity Linking in Multi-Party Dialogue. </span><em>Laura Aina, Carina Silberer, Ionut-Teodor Sorodoc, Matthijs Westera and Gemma Boleda</em></td></tr>
<tr id="poster" poster-id="1748"><td><span class="poster-title">Continuous Learning for Large-scale Personalized Domain Classification. </span><em>Han Li, Jihwan Lee, Sidharth Mudgal, Ruhi Sarikaya and Young-Bum Kim</em></td></tr>
<tr id="poster" poster-id="1974"><td><span class="poster-title">Cross-lingual Transfer Learning for Multilingual Task Oriented Dialog. </span><em>Sebastian Schuster, Sonal Gupta, Rushin Shah and Mike Lewis</em></td></tr>
<tr id="poster" poster-id="2139"><td><span class="poster-title">Evaluating Coherence in Dialogue Systems using Entailment. </span><em>Nouha Dziri, Ehsan Kamalloo, Kory Mathewson and Osmar Zaiane</em></td></tr>
<tr id="poster" poster-id="2399"><td><span class="poster-title">On Knowledge distillation from complex networks for response prediction. </span><em>Siddhartha Arora, Mitesh M. Khapra and Harish G. Ramaswamy</em></td></tr>
<tr><td><span class="poster-type">Multilingual NLP</span></td></tr>
<tr id="poster" poster-id="166"><td><span class="poster-title">Cross-lingual Multi-Level Adversarial Transfer to Enhance Low-Resource Name Tagging. </span><em>Lifu Huang, Heng Ji and Jonathan May</em></td></tr>
<tr id="poster" poster-id="255"><td><span class="poster-title">Unsupervised Extraction of Partial Translations for Neural Machine Translation. </span><em>Benjamin Marie and Atsushi Fujita</em></td></tr>
<tr id="poster" poster-id="377"><td><span class="poster-title">Low-Resource Syntactic Transfer with Unsupervised Source Reordering. </span><em>Mohammad Sadegh Rasooli and Michael Collins</em></td></tr>
<tr id="poster" poster-id="907"><td><span class="poster-title">Revisiting Adversarial Autoencoder for Unsupervised Word Translation with Cycle Consistency and Improved Training. </span><em>Tasnim Mohiuddin and Shafiq Joty</em></td></tr>
<tr id="poster" poster-id="1131"><td><span class="poster-title">Addressing word-order Divergence in Multilingual Neural Machine Translation for extremely Low Resource Languages. </span><em>Rudra Murthy, Anoop Kunchukuttan and Pushpak Bhattacharyya</em></td></tr>
<tr id="poster" poster-id="1206"><td><span class="poster-title">Massively Multilingual Neural Machine Translation. </span><em>Roee Aharoni, Melvin Johnson and Orhan Firat</em></td></tr>
<tr id="poster" poster-id="1229"><td><span class="poster-title">A Large-Scale Comparison of Historical Text Normalization Systems. </span><em> and Marcel Bollmann</em></td></tr>
<tr id="poster" poster-id="1351"><td><span class="poster-title">Combining Discourse Markers and Cross-lingual Embeddings for Synonym–Antonym Classification. </span><em>Michael Roth and Shyam Upadhyay</em></td></tr>
<tr id="poster" poster-id="1646"><td><span class="poster-title">Context-Aware Cross-Lingual Mapping. </span><em>Hanan Aldarmaki and Mona Diab</em></td></tr>
<tr id="poster" poster-id="1875"><td><span class="poster-title">Polyglot Contextual Representations Improve Crosslingual Transfer. </span><em>Phoebe Mulcaire, Jungo Kasai and Noah A. Smith</em></td></tr>
<tr id="poster" poster-id="2437"><td><span class="poster-title">Typological Features for Multilingual Delexicalised Dependency Parsing. </span><em>Manon Scholivet, Franck Dary, Alexis Nasr, Benoit Favre and Carlos Ramisch</em></td></tr>
<tr><td><span class="poster-type">Summarization</span></td></tr>
<tr id="poster" poster-id="397"><td><span class="poster-title">Recommendations for Datasets for Source Code Summarization. </span><em>Alexander LeClair and Collin McMillan</em></td></tr>
<tr id="poster" poster-id="458"><td><span class="poster-title">Question Answering as an Automatic Evaluation Metric for News Article Summarization. </span><em>Matan Eyal, Tal Baumel and Michael Elhadad</em></td></tr>
<tr id="poster" poster-id="700"><td><span class="poster-title">Understanding the Behaviour of Neural Abstractive Summarizers using Contrastive Examples. </span><em>Krtin Kumar and Jackie Chi Kit Cheung</em></td></tr>
<tr id="poster" poster-id="1096"><td><span class="poster-title">Jointly Extracting and Compressing Documents with Summary State Representations. </span><em>Afonso Mendes, Shashi Narayan, Sebastião Miranda, Zita Marinho, André F. T. Martins and Shay B. Cohen</em></td></tr>
<tr id="poster" poster-id="1621"><td><span class="poster-title">News Article Teaser Tweets and How to Generate Them. </span><em>Sanjeev Kumar Karn, Mark Buckley, Ulli Waltinger and Hinrich Schütze</em></td></tr>
<tr id="poster" poster-id="1694"><td><span class="poster-title">Cross-referencing Using Fine-grained Topic Modeling. </span><em>Jeffrey Lund, Piper Armstrong, Wilson Fearn, Stephen Cowley, Emily Hales and Kevin Seppi</em></td></tr>
<tr id="poster" poster-id="2197"><td><span class="poster-title">Conversation Initiation by Diverse News Contents Introduction. </span><em>Satoshi Akasaki and Nobuhiro Kaji</em></td></tr>
<tr id="poster" poster-id="2199"><td><span class="poster-title">Positional Encoding to Control Output Sequence Length. </span><em>Sho Takase and Naoaki Okazaki</em></td></tr>
</table>
</div>
</div>
</div>
<div class="session session-break session-plenary" id="session-break-14"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Wednesday, June 05, 2019">15:00 &ndash; 15:30</span></div>
<div class="session-box" id="session-box-9">
<div class="session-header" id="session-header-9">Short Orals / Industry Posters</div>
<div class="session session-expandable session-papers1" id="session-9a"><div id="expander"></div><a href="#" class="session-title">9A: Question Answering</a><br/><span class="session-time" title="Wednesday, June 05, 2019">15:30 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Greenway</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-9a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-9a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Mo Yu</td></tr>
<tr id="paper" paper-id="713"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">The Lower The Simpler: Simplifying Hierarchical Recurrent Models. </span><em>Chao Wang and Hui Jiang</em></td></tr>
<tr id="paper" paper-id="1355"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">Using Natural Language Relations between Answer Choices for Machine Comprehension. </span><em>Rajkumar Pujari and Dan Goldwasser</em></td></tr>
<tr id="paper" paper-id="1865"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">Saliency Learning: Teaching the Model Where to Pay Attention. </span><em>Reza Ghaeini, Xiaoli Fern, Hamed Shahbazi and Prasad Tadepalli</em></td></tr>
<tr id="paper" paper-id="2209"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">Understanding Dataset Design Choices for Multi-hop Reasoning. </span><em>Jifan Chen and Greg Durrett</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers2" id="session-9b"><div id="expander"></div><a href="#" class="session-title">9B: Applications</a><br/><span class="session-time" title="Wednesday, June 05, 2019">15:30 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Nicollet A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-9b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-9b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Zornitsa Kozareva</td></tr>
<tr id="paper" paper-id="619"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">Neural Grammatical Error Correction with Finite State Transducers. </span><em>Felix Stahlberg, Christopher Bryant and Bill Byrne</em></td></tr>
<tr id="paper" paper-id="1123"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">Convolutional Self-Attention Networks. </span><em>Baosong Yang, Longyue Wang, Derek F. Wong, Lidia S. Chao and Zhaopeng Tu</em></td></tr>
<tr id="paper" paper-id="1301"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">Rethinking Complex Neural Network Architectures for Document Classification. </span><em>Ashutosh Adhikari, Achyudh Ram, Raphael Tang and Jimmy Lin</em></td></tr>
<tr id="paper" paper-id="43-srw"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">Speak up, Fight Back! Detection of Social Media Disclosures of Sexual Harassment. </span><em>Arijit Ghosh Chowdhury, Ramit Sawhney, Puneet Mathur, Debanjan Mahata and Rajiv Ratn Shah</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers3" id="session-9c"><div id="expander"></div><a href="#" class="session-title">9C: Generation</a><br/><span class="session-time" title="Wednesday, June 05, 2019">15:30 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Northstar A</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-9c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-9c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Fei Liu</td></tr>
<tr id="paper" paper-id="1500"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">Pre-trained language model representations for language generation. </span><em>Sergey Edunov, Alexei Baevski and Michael Auli</em></td></tr>
<tr id="paper" paper-id="1968"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">Pragmatically Informative Text Generation. </span><em>Sheng Shen, Daniel Fried, Jacob Andreas and Dan Klein</em></td></tr>
<tr id="paper" paper-id="1991"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">Stochastic Wasserstein Autoencoder for Probabilistic Sentence Generation. </span><em>Hareesh Bahuleyan, Lili Mou, Hao Zhou and Olga Vechtomova</em></td></tr>
<tr id="paper" paper-id="2131"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">Benchmarking Hierarchical Script Knowledge. </span><em>Yonatan Bisk, Jan Buys, Karl Pichotta and Yejin Choi</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers4" id="session-9d"><div id="expander"></div><a href="#" class="session-title">9D: Cognitive  & Psycholinguistics</a><br/><span class="session-time" title="Wednesday, June 05, 2019">15:30 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Nicollet D</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-9d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-9d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Bridget McInnes</td></tr>
<tr id="paper" paper-id="45-srw"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">SNAP-BATNET: Cascading Author Profiling and Social Network Graphs for Suicide Ideation Detection on Social Media. </span><em>Rohan Mishra, Pradyumn Prakhar Sinha, Ramit Sawhney, Debanjan Mahata, Puneet Mathur and Rajiv Ratn Shah</em></td></tr>
<tr id="paper" paper-id="1479"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">A large-scale study of the effects of word frequency and predictability in naturalistic reading. </span><em> and Cory Shain</em></td></tr>
<tr id="paper" paper-id="1716"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">Augmenting word2vec with latent Dirichlet allocation within a clinical application. </span><em>Akshay Budhkar and Frank Rudzicz</em></td></tr>
<tr id="paper" paper-id="379"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">On the Idiosyncrasies of the Mandarin Chinese Classifier System. </span><em>Shijia Liu, Hongyuan Mei, Adina Williams and Ryan Cotterell</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-papers5" id="session-9e"><div id="expander"></div><a href="#" class="session-title">9E: Machine Learning</a><br/><span class="session-time" title="Wednesday, June 05, 2019">15:30 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Nicollet B+C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-9e-selector"> Choose All</a><a href="#" class="session-deselector" id="session-9e-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: Byron C. Wallace</td></tr>
<tr id="paper" paper-id="737"><td id="paper-time">15:30&ndash;15:45</td><td><span class="paper-title">Joint Learning of Pre-Trained and Random Units for Domain Adaptation in Part-of-Speech Tagging. </span><em>Sara Meftah, Youssef Tamaazousti, Nasredine Semmar, Hassane Essafi and Fatiha Sadat</em></td></tr>
<tr id="paper" paper-id="1051"><td id="paper-time">15:45&ndash;16:00</td><td><span class="paper-title">Show Some Love to Your n-grams: A Bit of Progress and Stronger n-gram Language Modeling Baselines. </span><em>Ehsan Shareghi, Daniela Gerz, Ivan Vulić and Anna Korhonen</em></td></tr>
<tr id="paper" paper-id="1307"><td id="paper-time">16:00&ndash;16:15</td><td><span class="paper-title">Training Data Augmentation for Context-Sensitive Neural Lemmatizer Using Inflection Tables and Raw Text. </span><em>Toms Bergmanis and Sharon Goldwater</em></td></tr>
<tr id="paper" paper-id="2342"><td id="paper-time">16:15&ndash;16:30</td><td><span class="paper-title">A Structural Probe for Finding Syntax in Word Representations. </span><em>John Hewitt and Christopher D. Manning</em></td></tr>
</table>
</div>
</div>
<div class="session session-expandable session-posters" id="session-poster-9"><div id="expander"></div><a href="#" class="session-title">9F: Industry (posters) </a><br/><span class="session-time" title="Wednesday, June 05, 2019">15:30 &ndash; 16:30</span><br/><span class="session-location btn btn--location">Hyatt Exhibit Hall</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="4109-industry"><td><span class="poster-title">Neural Lexicons for Slot Tagging in Spoken Language Understanding. </span><em> and Kyle Williams</em></td></tr>
<tr id="poster" poster-id="4010-industry"><td><span class="poster-title">Active Learning for New Domains in Natural Language Understanding. </span><em>Stanislav Peshterliev, John Kearney, Abhyuday Jagannatha, Imre Kiss and Spyros Matsoukas</em></td></tr>
<tr id="poster" poster-id="4090-industry"><td><span class="poster-title">Scaling Multi-Domain Dialogue State Tracking via Query Reformulation. </span><em>Pushpendre Rastogi, Arpit Gupta, Tongfei Chen and Mathias Lambert</em></td></tr>
<tr id="poster" poster-id="4101-industry"><td><span class="poster-title">Are the Tools up to the Task? an Evaluation of Commercial Dialog Tools in Developing Conversational Enterprise-grade Dialog Systems. </span><em>Marie Meteer, Meghan Hickey, Carmi Rothberg, David Nahamoo and Ellen Eide Kislal</em></td></tr>
<tr id="poster" poster-id="4063-industry"><td><span class="poster-title">Development and Deployment of a Large-Scale Dialog-based Intelligent Tutoring System. </span><em>Shazia Afzal, Tejas Dhamecha, Nirmal Mukhi, Renuka Sindhgatta, Smit Marvaniya, Matthew Ventura and Jessica Yarbro</em></td></tr>
<tr id="poster" poster-id="4022-industry"><td><span class="poster-title">Learning When Not to Answer: a Ternary Reward Structure for Reinforcement Learning Based Question Answering. </span><em>Fréderic Godin, Anjishnu Kumar and Arpit Mittal</em></td></tr>
<tr id="poster" poster-id="4131-industry"><td><span class="poster-title">Extraction of Message Sequence Charts from Software Use-Case Descriptions. </span><em>Girish Palshikar, Nitin Ramrakhiyani, Sangameshwar Patil, Sachin Pawar, Swapnil Hingmire, Vasudeva Varma and Pushpak Bhattacharyya</em></td></tr>
<tr id="poster" poster-id="4117-industry"><td><span class="poster-title">Improving Knowledge Base Construction from Robust Infobox Extraction. </span><em>Boya Peng, Yejin Huh, Xiao Ling and Michele Banko</em></td></tr>
<tr id="poster" poster-id="4100-industry"><td><span class="poster-title">A k-Nearest Neighbor Approach towards Multi-level Sequence Labeling. </span><em>Yue Chen and John Chen</em></td></tr>
<tr id="poster" poster-id="4082-industry"><td><span class="poster-title">Train One Get One Free: Partially Supervised Neural Network for Bug Report Duplicate Detection and Clustering. </span><em>Lahari Poddar, Leonardo Neves, William Brendel, Luis Marujo, Sergey Tulyakov and Pradeep Karuturi</em></td></tr>
<tr id="poster" poster-id="4083-industry"><td><span class="poster-title">Robust Semantic Parsing with Adversarial Learning for Domain Generalization. </span><em>Gabriel Marzinotto, Geraldine Damnati, Frederic Bechet and Benoit Favre</em></td></tr>
<tr id="poster" poster-id="4017-industry"><td><span class="poster-title">TOI-CNN: a Solution of Information Extraction on Chinese Insurance Policy. </span><em>Lin Sun, Kai Zhang, Fule Ji and Zhenhua Yang</em></td></tr>
<tr id="poster" poster-id="4006-industry"><td><span class="poster-title">Cross-lingual Transfer Learning for Japanese Named Entity Recognition. </span><em>Andrew Johnson, Penny Karanasou, Judith Gaspers and Dietrich Klakow</em></td></tr>
<tr id="poster" poster-id="4003-industry"><td><span class="poster-title">Neural Text Normalization with Subword Units. </span><em>Courtney Mansfield, Ming Sun, Yuzong Liu, Ankur Gandhe and Bjorn Hoffmeister</em></td></tr>
<tr id="poster" poster-id="4025-industry"><td><span class="poster-title">Audio De-identification - a New Entity Recognition Task. </span><em>Ido Cohn, Itay Laish, Genady Beryozkin, Gang Li, Izhak Shafran, Idan Szpektor, Tzvika Hartman, Avinatan Hassidim and Yossi Matias</em></td></tr>
<tr id="poster" poster-id="4054-industry"><td><span class="poster-title">In Other News: a Bi-style Text-to-speech Model for Synthesizing Newscaster Voice with Limited Data. </span><em>Nishant Prateek, Mateusz Łajszczak, Roberto Barra-Chicote, Thomas Drugman, Jaime Lorenzo-Trueba, Thomas Merritt, Srikanth Ronanki and Trevor Wood</em></td></tr>
<tr id="poster" poster-id="4058-industry"><td><span class="poster-title">Generate, Filter, and Rank: Grammaticality Classification for Production-Ready NLG Systems. </span><em>Ashwini Challa, Kartikeya Upasani, Anusha Balakrishnan and Rajen Subba</em></td></tr>
<tr id="poster" poster-id="4002-industry"><td><span class="poster-title">Content-based Dwell Time Engagement Prediction Model for News Articles. </span><em>Heidar Davoudi, Aijun An and Gordon Edall</em></td></tr>
</table>
</div>
</div>
</div>
<div class="session session-break session-plenary" id="session-break-15"><span class="session-title">Short Break</span><br/><span class="session-time" title="Wednesday, June 05, 2019">16:30 &ndash; 16:45</span></div>
<div class="session session-expandable session-papers-best"><div id="expander"></div><a href="#" class="session-title">Best Paper Session</a><br/><span class="session-time" title="Wednesday, June 05, 2019">16:45 &ndash; 18:15</span><br/><span class="session-location btn btn--location">Nicollet Grand Ballroom</span><br/><div class="paper-session-details"><br/><table class="paper-table">
<tr id="paper" paper-id="440"><td id="paper-time">16:45&ndash;17:03</td><td><span class="paper-title">CNM: An Interpretable Complex-valued Network for Matching. </span><em>Qiuchi Li, Benyou Wang and Massimo Melucci</em></td></tr>
<tr id="paper" paper-id="610"><td id="paper-time">17:03&ndash;17:21</td><td><span class="paper-title">CommonsenseQA: A Question Answering Challenge Targeting Commonsense Knowledge. </span><em>Alon Talmor, Jonathan Herzig, Nicholas Lourie and Jonathan Berant</em></td></tr>
<tr id="paper" paper-id="1458"><td id="paper-time">17:21&ndash;17:39</td><td><span class="paper-title">Probing the Need for Visual Context in Multimodal Machine Translation. </span><em>Ozan Caglayan, Pranava Madhyastha, Lucia Specia and Loïc Barrault</em></td></tr>
<tr id="paper" paper-id="1584"><td id="paper-time">17:39&ndash;17:57</td><td><span class="paper-title">BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. </span><em>Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova</em></td></tr>
<tr id="paper" paper-id="2035"><td id="paper-time">17:57&ndash;18:15</td><td><span class="paper-title">What’s in a Name? Reducing Bias in Bios without Access to Protected Attributes. </span><em>Alexey Romanov, Maria De-Arteaga, Hanna Wallach, Jennifer Chayes, Christian Borgs, Alexandra Chouldechova, Sahin Geyik, Krishnaram Kenthapadi, Anna Rumshisky and Adam Kalai</em></td></tr>
</table>
</div>
</div>
<div class="session session-plenary"><span class="session-title">Closing Remarks</span><br/><span class="session-time" title="Wednesday, June 05, 2019">18:15 &ndash; 18:30</span><br/><span class="session-location btn btn--location">Nicollet Grand Ballroom</span></div>
<div id="generatePDFForm">
<div id="formContainer">
<input type="checkbox" id="includePlenaryCheckBox" value="second_checkbox"/>&nbsp;&nbsp;<span id="checkBoxLabel">Include plenary sessions in schedule</span>
<br/>
<a href="#" id="generatePDFButton" class="btn btn--twitter btn--large">Download PDF</a></div>
</div>
</div>