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
                        if (cellText == "Break" || cellText == "Lunch" || cellText == "Breakfast" || cellText == "Coffee Break" || cellText == "Mini-Break") {
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
                        if (infoType == "info-plenary" && (infoText == "Break" || infoText == "Lunch" || infoText == "Breakfast" || infoText == "Coffee Break" || infoText == "Mini-Break")) {
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
{% include base_path %}
<link rel="stylesheet" href="/assets/css/alertify.css" id="alertifyCSS">

<table id="hidden-program-table">
    <thead>
        <tr><th>time</th><th>location</th><th>info</th></tr>
    </thead>
    <tbody></tbody>
</table>

<div id="introParagraph">
        <p>On this page, you can choose the sessions (and individual papers/posters) of your choice <em>and</em> generate a PDF of your customized schedule! This page should work on modern browsers on all operating systems. On mobile devices, Safari on iOS and Chrome on Android are the only browsers known to work. For the best experience, use a non-mobile device. For help, simply type "?"" while on the page or click on the "Help" button.</p>
        <p><strong>Note</strong>: To accommodate the large number of attendees, some sessions will be livestreamed into multiple rooms. For sessions listed with multiple rooms, the first room will have the actual presentations &amp; the rest will show a live-streamed feed of the presentations. Recorded videos for talks are linked below in the schedule. To request the removal of your video, contact the <a href="mailto:emnlp2018-video-chair@googlegroups.com">video chair</a>. Videos for the 3 tutorials on October 31st are unfortunately unavailable due to unforeseen issues with the videography.</p>
</div>

<p class="text-center">
    <a href="#" id="help-button" class="btn btn--small btn--twitter">Help</a>
</p>
<p class="text-center">
    <a href="#" id="toggle-all-button" class="btn btn--small btn--twitter">Expand All Sessions ↓</a>
</p>

<div class="schedule">
    <div class="day" id="first-day">Wednesday, October 31 2018</div>
    <div class="session session-expandable session-tutorials" id="session-morning-tutorials1">
        <div id="expander"></div><a href="#" class="session-title">Morning Tutorials</a><br/>
        <span class="session-time" title="Wednesday, October 31 2018">09:00 &ndash; 12:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T1] Joint Models for NLP.</strong> Yue Zhang. </span> <br/><span class="btn btn--location inline-location">Gold Hall</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T2] Graph Formalisms for Meaning Representations.</strong> Adam Lopez and Sorcha Gilroy.</span><br/><span href="#" class="btn btn--location inline-location">Hall 100</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-1">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time" title="Wednesday, October 31 2018">12:30 &ndash; 14:00</span>
    </div>    
    <div class="session session-expandable session-tutorials" id="session-afternoon-tutorials1">
        <div id="expander"></div><a href="#" class="session-title">Afternoon Tutorials</a><br/>
        <span class="session-time" title="Wednesday, October 31 2018">14:00 &ndash; 17:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T3] Writing Code for NLP Research.</strong> Matt Gardner, Mark Neumann, Joel Grus, and Nicholas Lourie. </span><br/><span href="#" class="btn btn--location inline-location">Gold Hall</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-workshops" id="session-workshops-1">
        <div id="expander"></div><a href="#" class="session-title">Workshops &amp; Co-located Events</a><br/>
        <span class="session-time" title="Wednesday, October 31 2018">08:30 &ndash; 18:00</span><br/>
        <div class="workshop-session-details">
            <br/>
            <table class="workshop-table">
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W1] WMT18: The Third Conference on Machine Translation (Day 1).</strong> </span> <br/><span class="btn btn--location inline-location">Bozar Hall (Salle M)</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W2] CoNLL: The Conference on Computational Natural Language Learning (Day 1).</strong> </span> <br/><span class="btn btn--location inline-location">Copper Hall / Studio 311 &ndash; 312</span>
                    </td>
                </tr>                
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W3] LOUHI: The Ninth International Workshop on Health Text Mining and Information Analysis.</strong> </span> <br/><span class="btn btn--location inline-location">The Arc</span>
                    </td>
                </tr> 
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W4] ALW2: Second Workshop on Abusive Language Online.</strong> </span> <br/><span class="btn btn--location inline-location">Studio 211 &ndash; 212</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W5] SCAI: Search-Oriented Conversational AI.</strong> </span> <br/><span class="btn btn--location inline-location">Silver Hall / Studio 313 &ndash; 315</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W6] SIGMORPHON: Fifteenth Workshop on Computational Research in Phonetics, Phonology, and Morphology.</strong> </span> <br/><span class="btn btn--location inline-location">Studio 213 &ndash; 215</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W7] WASSA: 9th Workshop on Computational Approaches to Subjectivity, Sentiment and Social Media Analysis.</strong> </span> <br/><span class="btn btn--location inline-location">Hall 400</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W8] SMM4H: 3rd Workshop on Social Media Mining for Health Applications Workshop & Shared Task.</strong> </span> <br/><span class="btn btn--location inline-location">Studio 201A/B</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="day" id="second-day">Thursday, November 1 2018</div>
    <div class="session session-expandable session-tutorials" id="session-morning-tutorials2">
        <div id="expander"></div><a href="#" class="session-title">Morning Tutorials</a><br/>
        <span class="session-time" title="Thursday, November 1 2018">09:00 &ndash; 12:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T4] Deep Latent Variable Models of Natural Language.</strong> Alexander Rush, Yoon Kim, and Sam Wiseman. &nbsp;<i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305182667" aria-hidden="true" title="Video"></i></span> <br/><span class="btn btn--location inline-location">Gold Hall</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T5] Standardized Tests as benchmarks for Artificial Intelligence.</strong> Mrinmaya Sachan, Minjoon Seo, Hannaneh Hajishirzi, and Eric Xing. &nbsp;<i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305187739" aria-hidden="true" title="Video"></i></span><br/><span href="#" class="btn btn--location inline-location">Hall 400</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-2">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time" title="Thursday, November 1 2018">12:30 &ndash; 14:00</span>
    </div>    
    <div class="session session-expandable session-tutorials" id="session-afternoon-tutorials2">
        <div id="expander"></div><a href="#" class="session-title">Afternoon Tutorials</a><br/>
        <span class="session-time" title="Thursday, November 1 2018">14:00 &ndash; 17:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T6] Deep Chit-Chat: Deep Learning for ChatBots.</strong> Wei Wu and Rui Yan. &nbsp;<i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305179403" aria-hidden="true" title="Video"></i></span><br/><span href="#" class="btn btn--location inline-location">Gold Hall</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-workshops" id="session-workshops-2">
        <div id="expander"></div><a href="#" class="session-title">Workshops &amp; Co-located Events</a><br/>
        <span class="session-time" title="Thursday, November 1 2018">09:00 &ndash; 17:00</span><br/>
        <div class="workshop-session-details">
            <br/>
            <table class="workshop-table">
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W1] WMT18: The Third Conference on Machine Translation (Day 2).</strong> </span> <br/><span class="btn btn--location inline-location">Bozar Hall (Salle M)</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W2] CoNLL: The Conference on Computational Natural Language Learning (Day 2).</strong> </span> <br/><span class="btn btn--location inline-location">Copper Hall / Studio 311 &ndash; 312</span>
                    </td>
                </tr>                
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W9] BioASQ: Large-scale Biomedical Semantic Indexing and Question Answering.</strong> </span> <br/><span class="btn btn--location inline-location">Studio 313 &ndash; 315</span>
                    </td>
                </tr> 
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W10] BlackboxNLP: Analyzing and Interpreting Neural Networks for NLP.</strong> </span> <br/><span class="btn btn--location inline-location">Silver Hall / Hall 100</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W11] FEVER: First Workshop on Fact Extraction and VERification.</strong> </span> <br/><span class="btn btn--location inline-location">The Arc</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W12] ARGMINING: 5th International Workshop on Argument Mining.</strong> </span> <br/><span class="btn btn--location inline-location">Studio 213 &ndash; 215</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W13] W-NUT: 4th Workshop on Noisy User-generated Text.</strong> </span> <br/><span class="btn btn--location inline-location">Panoramic Hall</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W14] UDW-18: Second Workshop on Universal Dependencies.</strong> </span> <br/><span class="btn btn--location inline-location">Studio 201A/B</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-plenary" id="session-reception">
        <div id="expander"></div>
        <a href="#" class="session-title">Welcome Reception</a>
        <br/>
        <span class="session-time" title="Thursday, November 1 2018">18:00 &ndash; 20:00</span>
        <br/>
        <span class="session-location btn btn--location">Grand Hall</span>
        <div class="paper-session-details">
            <br/><br/>
            <div class="session-abstract">
                <p>Catch up with your colleagues at the Welcome Reception! It will be held immediately following the tutorials on Thursday, November 1st. <br/>Appetizers and refreshments will be provided.</p>
            </div>
        </div>
    </div>
    <div class="day" id="day-3">Friday, 2 November 2018</div>
    <div class="session session-plenary" id="session-welcome">
        <span class="session-title">Opening remarks</span>
        <br/>
        <span class="session-time" title="Friday, 2 November 2018">09:00 &ndash; 09:30</span>
        <br/>
        <span class="session-location btn btn--location">Gold Hall / Copper Hall / Silver Hall / Hall 100</span>
    </div>
    <div class="session session-expandable session-plenary">
        <div id="expander"></div>
        <a href="#" class="session-title">
            <strong>Keynote I: "Truth or Lie? Spoken Indicators of Deception in Speech"</strong>
        </a>
        <br/>
        <span class="session-people">
            <a href="http://www.cs.columbia.edu/~julia/" target="_blank">Julia Hirschberg (Columbia University)</a>
        </span>
        <br/>
        <span class="session-time" title="Friday, 2 November 2018">09:30 &ndash; 10:30</span>
        <br/>
        <span class="session-location btn btn--location">Gold Hall / Copper Hall / Silver Hall / Hall 100</span>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">
                <p>Detecting deception from various forms of human behavior is a longstanding research goal which is of considerable interest to the military, law enforcement, corporate security, social services and mental health workers. However, both humans and polygraphs are very poor at this task. We describe more accurate methods we have developed to detect deception automatically from spoken language. Our classifiers are trained on the largest cleanly recorded corpus of within-subject deceptive and non-deceptive speech that has been collected. To distinguish truth from lie we make use of acoustic-prosodic, lexical, demographic, and personality features. We further examine differences in deceptive behavior based upon gender, personality, and native language (Mandarin Chinese vs. English), comparing our systems to human performance. We extend our studies to identify cues in trusted speech vs. mistrusted speech and how these features differ by speaker and by listener. Why does a listener believe a lie?&nbsp;
                    <i class="fa fa-television slides-icon" data="/downloads/keynote-slides/JuliaHirschberg.pdf" aria-hidden="true" title="Slides"></i>&nbsp;
                    <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305200179" aria-hidden="true" title="Video"></i>
                </p>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-1">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time" title="Friday, 2 November 2018">10:30 &ndash; 11:00</span>
    </div>
    <div class="session-box" id="session-box-1">
        <div class="session-header" id="session-header-1">Long Papers &amp; Demos I (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-1a">
            <div id="expander"></div>
            <a href="#" class="session-title">1A: Social Applications I</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-1a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-1a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:mail@dirkhovy.com">Dirk Hovy</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="523">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">Privacy-preserving Neural Representations of Text.</span>
                            <em>Maximin Coavoux, Shashi Narayan and Shay B. Cohen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1001" aria-hidden="true" title="PDF"></i>&nbsp;
                        </td>
                    </tr>
                    <tr id="paper" paper-id="888">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">Adversarial Removal of Demographic Attributes from Text Data.</span>
                            <em>Yanai Elazar and Yoav Goldberg</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1002" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305203150" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="909">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">DeClarE: Debunking Fake News and False Claims using Evidence-Aware Deep Learning.</span>
                            <em>Kashyap Popat, Subhabrata Mukherjee, Andrew Yates and Gerhard Weikum</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1003" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305203523" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1879">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">It's going to be okay: Measuring Access to Support in Online Communities.</span>
                            <em>Zijian Wang and David Jurgens</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1004" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305203914" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1903">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Detecting Gang-Involved Escalation on Social Media Using Context.</span>
                            <em>Serina Chang, Ruiqi Zhong, Ethan Adams, Fei-Tzin Lee, Siddharth Varia, Desmond Patton, William Frey, Chris Kedzie and Kathy McKeown</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1005" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305204297" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-1b">
            <div id="expander"></div>
            <a href="#" class="session-title">1B: Semantics I</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-1b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-1b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:natschluter@itu.dk">Natalie Schluter</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1172">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">Reasoning about Actions and State Changes by Injecting Commonsense Knowledge.</span>
                            <em>Niket Tandon, Bhavana Dalvi, Joel Grus, Wen-tau Yih, Antoine Bosselut and Peter Clark</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1006" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305193585" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1494">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">Collecting Diverse Natural Language Inference Problems for Sentence Representation Evaluation.</span>
                            <em>Adam Poliak, Aparajita Haldar, Rachel Rudinger, J. Edward Hu, Ellie Pavlick, Aaron Steven White and Benjamin Van Durme</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1007" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305194062" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1634">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">Textual Analogy Parsing: What's Shared and What's Compared among Analogous Facts.</span>
                            <em>Matthew Lamm, Arun Chaganty, Christopher D. Manning, Dan Jurafsky and Percy Liang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1008" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305194870" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2020">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">SWAG: A Large-Scale Adversarial Dataset for Grounded Commonsense Inference.</span>
                            <em>Rowan Zellers, Yonatan Bisk, Roy Schwartz and Yejin Choi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1009" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305195438" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2036">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TwoWingOS: A Two-Wing Optimization Strategy for Evidential Claim Verification.</span>
                            <em>Wenpeng Yin and Dan Roth</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1010" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305195990" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-1c">
            <div id="expander"></div>
            <a href="#" class="session-title">1C: Vision</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-1c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-1c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:g.chrupala@uvt.nl">Grzegorz Chrupała</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="201">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">Associative Multichannel Autoencoder for Multimodal Word Representation.</span>
                            <em>Shaonan Wang, Jiajun Zhang and Chengqing Zong</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1011" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305209813" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="576">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">Game-Based Video-Context Dialogue.</span>
                            <em>Ramakanth Pasunuru and Mohit Bansal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1012" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305210347" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="836">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">simNet: Stepwise Image-Topic Merging Network for Generating Detailed and Comprehensive Image Captions.</span>
                            <em>Fenglin Liu, Xuancheng Ren, Yuanxin Liu, Houfeng Wang and Xu Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1013" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305210529" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1792">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Multimodal Language Analysis with Recurrent Multistage Fusion.</span>
                            <em>Paul Pu Liang, Ziyin Liu, AmirAli Bagher Zadeh and Louis-Philippe Morency</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1014" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305210831" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1845">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Temporally Grounding Natural Sentence in Video.</span>
                            <em>Jingyuan Chen, Xinpeng Chen, Lin Ma, Zequn Jie and Tat-Seng Chua</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1015" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305211326" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-1d">
            <div id="expander"></div>
            <a href="#" class="session-title">1D: Entities &amp; Coreference</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-1d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-1d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:eduardo.blanco@unt.edu">Eduardo Blanco</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="392">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">PreCo: A Large-scale Dataset in Preschool Vocabulary for Coreference Resolution.</span>
                            <em>Hong Chen, Zhenhua Fan, Hao Lu, Alan Yuille and Shu Rong</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1016" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306353798" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="627">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">Adversarial Transfer Learning for Chinese Named Entity Recognition with Self-Attention Mechanism.</span>
                            <em>Pengfei Cao, Yubo Chen, Kang Liu, Jun Zhao and Shengping Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1017" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306354811" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1286">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">Using Linguistic Features to Improve the Generalization Capability of Neural Coreference Resolvers.</span>
                            <em>Nafise Sadat Moosavi and Michael Strube</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1018" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306355512" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1574">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Neural Segmental Hypergraphs for Overlapping Mention Recognition.</span>
                            <em>Bailin Wang and Wei Lu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1019" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306356485" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1846">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Variational Sequential Labelers for Semi-Supervised Learning.</span>
                            <em>Mingda Chen, Qingming Tang, Karen Livescu and Kevin Gimpel</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1020" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306357379" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-1">
            <div id="expander"></div>
            <a href="#" class="session-title">1E: Machine Translation &amp; Multilingual Methods (Posters and Demos)</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Multilingual Methods</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="76">
                        <td>
                            <span class="poster-title">Joint Representation Learning of Cross-lingual Words and Entities via Attentive Distant Supervision.</span>
                            <em>Yixin Cao, Lei Hou, Juanzi Li, Zhiyuan Liu, Chengjiang Li, Xu Chen and Tiansi Dong</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1021" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="126">
                        <td>
                            <span class="poster-title">Deep Pivot-Based Modeling for Cross-language Cross-domain Transfer with Minimal Guidance.</span>
                            <em>Yftah Ziser and Roi Reichart</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1022" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="270">
                        <td>
                            <span class="poster-title">Multi-lingual Common Semantic Space Construction via Cluster-consistent Word Embedding.</span>
                            <em>Lifu Huang, Kyunghyun Cho, Boliang Zhang, Heng Ji and Kevin Knight</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1023" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="344">
                        <td>
                            <span class="poster-title">Unsupervised Multilingual Word Embeddings.</span>
                            <em>Xilun Chen and Claire Cardie</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1024" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="517">
                        <td>
                            <span class="poster-title">CLUSE: Cross-Lingual Unsupervised Sense Embeddings.</span>
                            <em>Ta Chung Chi and Yun-Nung Chen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1025" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1036">
                        <td>
                            <span class="poster-title">Adversarial Propagation and Zero-Shot Cross-Lingual Transfer of Word Vector Specialization.</span>
                            <em>Edoardo Maria Ponti, Ivan Vulić, Goran Glavaš, Nikola Mrkšić and Anna Korhonen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1026" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1093">
                        <td>
                            <span class="poster-title">Improving Cross-Lingual Word Embeddings by Meeting in the Middle.</span>
                            <em>Yerai Doval, Jose Camacho-Collados, Luis Espinosa Anke and Steven Schockaert</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1027" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1134">
                        <td>
                            <span class="poster-title">WikiAtomicEdits: A Multilingual Corpus of Wikipedia Edits for Modeling Language and Discourse.</span>
                            <em>Manaal Faruqui, Ellie Pavlick, Ian Tenney and Dipanjan Das</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1028" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1301">
                        <td>
                            <span class="poster-title">On the Relation between Linguistic Typology and (Limitations of) Multilingual Language Modeling.</span>
                            <em>Daniela Gerz, Ivan Vulić, Edoardo Maria Ponti, Roi Reichart and Anna Korhonen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1029" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1439">
                        <td>
                            <span class="poster-title">A Fast, Compact, Accurate Model for Language Identification of Codemixed Text.</span>
                            <em>Yuan Zhang, Jason Riesa, Daniel Gillick, Anton Bakalov, Jason Baldridge and David Weiss</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1030" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1502">
                        <td>
                            <span class="poster-title">Personalized Microblog Sentiment Classification via Adversarial Cross-lingual Multi-task Learning.</span>
                            <em>Weichao Wang, Shi Feng, Wei Gao, Daling Wang and Yifei Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1031" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2115">
                        <td>
                            <span class="poster-title">Cross-lingual Knowledge Graph Alignment via Graph Convolutional Networks.</span>
                            <em>Zhichun Wang, Qingsong Lv, Xiaohan Lan and Yu Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1032" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2122">
                        <td>
                            <span class="poster-title">Cross-lingual Lexical Sememe Prediction.</span>
                            <em>Fanchao Qi, Yankai Lin, Maosong Sun, Hao Zhu, Ruobing Xie and Zhiyuan Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1033" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2268">
                        <td>
                            <span class="poster-title">Neural Cross-Lingual Named Entity Recognition with Minimal Resources.</span>
                            <em>Jiateng Xie, Zhilin Yang, Graham Neubig, Noah A. Smith and Jaime Carbonell</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1034" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Machine Translation</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="310">
                        <td>
                            <span class="poster-title">A Stable and Effective Learning Strategy for Trainable Greedy Decoding.</span>
                            <em>Yun Chen, Victor O.K. Li, Kyunghyun Cho and Samuel Bowman</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1035" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="349">
                        <td>
                            <span class="poster-title">Addressing Troublesome Words in Neural Machine Translation.</span>
                            <em>Yang Zhao, Jiajun Zhang, Zhongjun He, Chengqing Zong and Hua Wu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1036" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="566">
                        <td>
                            <span class="poster-title">Top-down Tree Structured Decoding with Syntactic Connections for Neural Machine Translation and Parsing.</span>
                            <em>Jetic Gū, Hassan S. Shavarani and Anoop Sarkar</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1037" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="643">
                        <td>
                            <span class="poster-title">XL-NBT: A Cross-lingual Neural Belief Tracking Framework.</span>
                            <em>Wenhu Chen, Jianshu Chen, Yu Su, Xin Wang, Dong Yu, Xifeng Yan and William Yang Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1038" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="683">
                        <td>
                            <span class="poster-title">Contextual Parameter Generation for Universal Neural Machine Translation.</span>
                            <em>Emmanouil Antonios Platanios, Mrinmaya Sachan, Graham Neubig and Tom Mitchell</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1039" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1069">
                        <td>
                            <span class="poster-title">Back-Translation Sampling by Targeting Difficult Words in Neural Machine Translation.</span>
                            <em>Marzieh Fadaee and Christof Monz</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1040" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1107">
                        <td>
                            <span class="poster-title">Multi-Domain Neural Machine Translation with Word-Level Domain Context Discrimination.</span>
                            <em>Jiali Zeng, Jinsong Su, Huating Wen, Yang Liu, Jun Xie, Yongjing Yin and Jianqiang Zhao</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1041" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1116">
                        <td>
                            <span class="poster-title">A Discriminative Latent-Variable Model for Bilingual Lexicon Induction.</span>
                            <em>Sebastian Ruder, Ryan Cotterell, Yova Kementchedjhieva and Anders Søgaard</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1042" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1436">
                        <td>
                            <span class="poster-title">Non-Adversarial Unsupervised Word Translation.</span>
                            <em>Yedid Hoshen and Lior Wolf</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1043" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1536">
                        <td>
                            <span class="poster-title">Semi-Autoregressive Neural Machine Translation.</span>
                            <em>Chunqi Wang, Ji Zhang and Haiqing Chen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1044" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1542">
                        <td>
                            <span class="poster-title">Understanding Back-Translation at Scale.</span>
                            <em>Sergey Edunov, Myle Ott, Michael Auli and David Grangier</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1045" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1894">
                        <td>
                            <span class="poster-title">Bootstrapping Transliteration with Constrained Discovery for Low-Resource Languages.</span>
                            <em>Shyam Upadhyay, Jordan Kodner and Dan Roth</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1046" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1948">
                        <td>
                            <span class="poster-title">NORMA: Neighborhood Sensitive Maps for Multilingual Word Embeddings.</span>
                            <em>Ndapa Nakashole</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1047" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1952">
                        <td>
                            <span class="poster-title">Adaptive Multi-pass Decoder for Neural Machine Translation.</span>
                            <em>Xinwei Geng, Xiaocheng Feng, Bing Qin and Ting Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1048" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2056">
                        <td>
                            <span class="poster-title">Improving the Transformer Translation Model with Document-Level Context.</span>
                            <em>Jiacheng Zhang, Huanbo Luan, Maosong Sun, Feifei Zhai, Jingfang Xu, Min Zhang and Yang Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1049" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2139">
                        <td>
                            <span class="poster-title">MTNT: A Testbed for Machine Translation of Noisy Text.</span>
                            <em>Paul Michel and Graham Neubig</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1050" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Demos</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="65-demo">
                        <td>
                            <span class="poster-title">CytonMT: an Efficient Neural Machine Translation Open-source Toolkit Implemented in C++.</span>
                            <em>Xiaolin Wang, Masao Utiyama and Eiichiro Sumita</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2023" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="38-demo">
                        <td>
                            <span class="poster-title">SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing.</span>
                            <em>Taku Kudo and John Richardson</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2012" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-3">
        <span class="session-title">Lunch</span>
        <br/>
        <span class="session-time" title="Friday, 2 November 2018">12:30 &ndash; 13:45</span>
    </div>
    <div class="session-box" id="session-box-2">
        <div class="session-header" id="session-header-2">Short Papers I (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-2a">
            <div id="expander"></div>
            <a href="#" class="session-title">2A: Question Answering I</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-2a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-2a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:scottyih@allenai.org">Scott Wen-tau Yih</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="592">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">SimpleQuestions Nearly Solved: A New Upperbound and Baseline Approach.</span>
                            <em>Michael Petrochuk and Luke Zettlemoyer</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1051" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305204813" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1649">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Phrase-Indexed Question Answering: A New Challenge for Scalable Document Comprehension.</span>
                            <em>Minjoon Seo, Tom Kwiatkowski, Ankur Parikh, Ali Farhadi and Hannaneh Hajishirzi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1052" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305205055" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="418">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">Ranking Paragraphs for Improving Answer Recall in Open-Domain Question Answering.</span>
                            <em>Jinhyuk Lee, Seongjun Yun, Hyunjae Kim, Miyoung Ko and Jaewoo Kang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1053" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305205289" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="131">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Cut to the Chase: A Context Zoom-in Network for Reading Comprehension.</span>
                            <em>Sathish Reddy Indurthi, Seunghak Yu, Seohyun Back and Heriberto Cuayahuitl</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1054" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305205548" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="940">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">Adaptive Document Retrieval for Deep Question Answering.</span>
                            <em>Bernhard Kratzwald and Stefan Feuerriegel</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1055" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305205847" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-2b">
            <div id="expander"></div>
            <a href="#" class="session-title">2B: Semantics II</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-2b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-2b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:xu.1265@osu.edu">Wei Xu</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1297">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">Why is unsupervised alignment of English embeddings from different algorithms so hard?.</span>
                            <em>Mareike Hartmann, Yova Kementchedjhieva and Anders Søgaard</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1056" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305196498" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2091">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Quantifying Context Overlap for Training Word Embeddings.</span>
                            <em>Yimeng Zhuang, Jinghui Xie, Yinhe Zheng and Xuan Zhu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1057" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305196755" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="203">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">Neural Latent Relational Analysis to Capture Lexical Semantic Relations in a Vector Space.</span>
                            <em>Koki Washio and Tsuneaki Kato</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1058" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305197006" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2267">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Generalizing Word Embeddings using Bag of Subwords.</span>
                            <em>Jinman Zhao, Sidharth Mudgal and Yingyu Liang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1059" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305197257" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2075">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">Neural Metaphor Detection in Context.</span>
                            <em>Ge Gao, Eunsol Choi, Yejin Choi and Luke Zettlemoyer</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1060" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305197464" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-2c">
            <div id="expander"></div>
            <a href="#" class="session-title">2C: Multilingual Methods I</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-2c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-2c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:shacharmirkin@gmail.com">Shachar Mirkin</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1376">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">Distant Supervision from Disparate Sources for Low-Resource Part-of-Speech Tagging.</span>
                            <em>Barbara Plank and Željko Agić</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1061" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305211701" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="446">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Unsupervised Bilingual Lexicon Induction via Latent Variable Models.</span>
                            <em>Zi-Yi Dou, Zhi-Hao Zhou and Shujian Huang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1062" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305211999" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1434">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">Learning Unsupervised Word Translations Without Adversaries.</span>
                            <em>Tanmoy Mukherjee, Makoto Yamada and Timothy Hospedales</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1063" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305212238" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="728">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Adversarial Training for Multi-task and Multi-lingual Joint Modeling of Utterance Intent Classification.</span>
                            <em>Ryo Masumura, Yusuke Shinohara, Ryuichiro Higashinaka and Yushi Aono</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1064" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305212477" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1462">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">Surprisingly Easy Hard-Attention for Sequence to Sequence Learning.</span>
                            <em>Shiv Shankar, Siddhant Garg and Sunita Sarawagi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1065" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305212816" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-2d">
            <div id="expander"></div>
            <a href="#" class="session-title">2D: Social Media</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-2d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-2d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:luwang@ccs.neu.edu">Lu Wang</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="977">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">Joint Learning for Emotion Classification and Emotion Cause Detection.</span>
                            <em>Ying Chen, Wenjun Hou, Xiyao Cheng and Shoushan Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1066" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306358514" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2240">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Exploring Optimism and Pessimism in Twitter Using Deep Learning.</span>
                            <em>Cornelia Caragea, Liviu P. Dinu and Bogdan Dumitru</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1067" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306359438" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2004">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">Predicting News Headline Popularity with Syntactic and Semantic Knowledge Using Multi-Task Learning.</span>
                            <em>Sotiris Lamprinidis, Daniel Hardt and Dirk Hovy</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1068" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306360116" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="468">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Hybrid Neural Attention for Agreement/Disagreement Inference in Online Debates.</span>
                            <em>Di Chen, Jiachen Du, Lidong Bing and Ruifeng Xu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1069" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306360792" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="794">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">Increasing In-Class Similarity by Retrofitting Embeddings with Demographic Information.</span>
                            <em>Dirk Hovy and Tommaso Fornaciari</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1070" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306361301" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-2">
            <div id="expander"></div>
            <a href="#" class="session-title">2E: Short Posters I</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Dialogue and Discourse</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="53">
                        <td>
                            <span class="poster-title">A Syntactically Constrained Bidirectional-Asynchronous Approach for Emotional Conversation Generation.</span>
                            <em>Jingyuan Li and Xiao Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1071" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="501">
                        <td>
                            <span class="poster-title">Auto-Dialabel: Labeling Dialogue Data with Unsupervised Learning.</span>
                            <em>Chen Shi, Qi Chen, Lei Sha, Sujian Li, Xu Sun, Houfeng Wang and Lintao Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1072" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="679">
                        <td>
                            <span class="poster-title">Extending Neural Generative Conversational Model using External Knowledge Sources.</span>
                            <em>Prasanna Parthasarathi and Joelle Pineau</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1073" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1435">
                        <td>
                            <span class="poster-title">Modeling Temporality of Human Intentions by Domain Adaptation.</span>
                            <em>Xiaolei Huang, Lixing Liu, Kate Carey, Joshua Woolley, Stefan Scherer and Brian Borsari</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1074" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1642">
                        <td>
                            <span class="poster-title">An Auto-Encoder Matching Model for Learning Utterance-Level Semantic Dependency in Dialogue Generation.</span>
                            <em>Liangchen Luo, Jingjing Xu, Junyang Lin, Qi Zeng and Xu Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1075" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1740">
                        <td>
                            <span class="poster-title">A Dataset for Document Grounded Conversations.</span>
                            <em>Kangyan Zhou, Shrimai Prabhumoye and Alan W Black</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1076" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="895">
                        <td>
                            <span class="poster-title">Out-of-domain Detection based on Generative Adversarial Network.</span>
                            <em>Seonghan Ryu, Sangjun Koo, Hwanjo Yu and Gary Geunbae Lee</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1077" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1085">
                        <td>
                            <span class="poster-title">Listening Comprehension over Argumentative Content.</span>
                            <em>Shachar Mirkin, Guy Moshkowich, Matan Orbach, Lili Kotlerman, Yoav Kantor, Tamar Lavee, Michal Jacovi, Yonatan Bilu, Ranit Aharonov and Noam Slonim</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1078" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="333">
                        <td>
                            <span class="poster-title">Using active learning to expand training data for implicit discourse relation recognition.</span>
                            <em>Yang Xu, Yu Hong, Huibin Ruan, Jianmin Yao, Min Zhang and Guodong Zhou</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1079" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Generation and Summarization</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1474">
                        <td>
                            <span class="poster-title">Learning To Split and Rephrase From Wikipedia Edit History.</span>
                            <em>Jan A. Botha, Manaal Faruqui, John Alex, Jason Baldridge and Dipanjan Das</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1080" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="887">
                        <td>
                            <span class="poster-title">BLEU is Not Suitable for the Evaluation of Text Simplification.</span>
                            <em>Elior Sulem, Omri Abend and Ari Rappoport</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1081" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2142">
                        <td>
                            <span class="poster-title">S2SPMN: A Simple and Effective Framework for Response Generation with Relevant Information.</span>
                            <em>Jiaxin Pei and Chenliang Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1082" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="213">
                        <td>
                            <span class="poster-title">Improving Reinforcement Learning Based Image Captioning with Natural Language Prior.</span>
                            <em>Tszhang Guo, Shiyu Chang, Mo Yu and Kun Bai</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1083" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1538">
                        <td>
                            <span class="poster-title">Training for Diversity in Image Paragraph Captioning.</span>
                            <em>Luke Melas-Kyriazi, Alexander Rush and George Han</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1084" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="318">
                        <td>
                            <span class="poster-title">A Graph-theoretic Summary Evaluation for ROUGE.</span>
                            <em>Elaheh ShafieiBavani, Mohammad Ebrahimi, Raymond Wong and Fang Chen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1085" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1156">
                        <td>
                            <span class="poster-title">Guided Neural Language Generation for Abstractive Summarization using Abstract Meaning Representation.</span>
                            <em>Hardy Hardy and Andreas Vlachos</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1086" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1544">
                        <td>
                            <span class="poster-title">Evaluating Multiple System Summary Lengths: A Case Study.</span>
                            <em>Ori Shapira, David Gabay, Hadar Ronen, Judit Bar-Ilan, Yael Amsterdamer, Ani Nenkova and Ido Dagan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1087" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1617">
                        <td>
                            <span class="poster-title">Neural Latent Extractive Document Summarization.</span>
                            <em>Xingxing Zhang, Mirella Lapata, Furu Wei and Ming Zhou</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1088" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2242">
                        <td>
                            <span class="poster-title">On the Abstractiveness of Neural Document Summarization.</span>
                            <em>Fangfang Zhang, Jin-ge Yao and Rui Yan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1089" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Text Classification, Text Mining and Information Retrieval</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1774">
                        <td>
                            <span class="poster-title">Automatic Essay Scoring Incorporating Rating Schema via Reinforcement Learning.</span>
                            <em>Yucheng Wang, Zhongyu Wei, Yaqian Zhou and Xuanjing Huang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1090" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="16">
                        <td>
                            <span class="poster-title">Identifying Well-formed Natural Language Questions.</span>
                            <em>Manaal Faruqui and Dipanjan Das</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1091" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="747">
                        <td>
                            <span class="poster-title">Self-Governing Neural Networks for On-Device Short Text Classification.</span>
                            <em>Sujith Ravi and Zornitsa Kozareva</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1105" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="865">
                        <td>
                            <span class="poster-title">HFT-CNN: Learning Hierarchical Category Structure for Multi-label Short Text Categorization.</span>
                            <em>Kazuya Shimura, Jiyi Li and Fumiyo Fukumoto</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1093" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1095">
                        <td>
                            <span class="poster-title">A Hierarchical Neural Attention-based Text Classifier.</span>
                            <em>Koustuv Sinha, Yue Dong, Jackie Chi Kit Cheung and Derek Ruths</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1094" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2181">
                        <td>
                            <span class="poster-title">Labeled Anchors and a Scalable, Transparent, and Interactive Classifier.</span>
                            <em>Jeffrey Lund, Stephen Cowley, Wilson Fearn, Emily Hales and Kevin Seppi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1095" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="577">
                        <td>
                            <span class="poster-title">Coherence-Aware Neural Topic Modeling.</span>
                            <em>Ran Ding, Ramesh Nallapati and Bing Xiang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1096" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1031">
                        <td>
                            <span class="poster-title">Utilizing Character and Word Embeddings for Text Normalization with Sequence-to-Sequence Models.</span>
                            <em>Daniel Watson, Nasser Zalmout and Nizar Habash</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1097" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1549">
                        <td>
                            <span class="poster-title">Topic Intrusion for Automatic Topic Model Evaluation.</span>
                            <em>Shraey Bhatia, Jey Han Lau and Timothy Baldwin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1098" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1726">
                        <td>
                            <span class="poster-title">Supervised and Unsupervised Methods for Robust Separation of Section Titles and Prose Text in Web Documents.</span>
                            <em>Abhijith Athreya Mysore Gopinath, Shomir Wilson and Norman Sadeh</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1099" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-2">
        <span class="session-title">Mini-Break</span>
        <br/>
        <span class="session-time" title="Friday, 2 November 2018">14:45 &ndash; 15:00</span>
    </div>
    <div class="session-box" id="session-box-3">
        <div class="session-header" id="session-header-3">Short Papers II (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-3a">
            <div id="expander"></div>
            <a href="#" class="session-title">3A: Machine Translation I</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-3a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-3a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:l.specia@sheffield.ac.uk">Lucia Specia</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1527">
                        <td id="paper-time">15:00&ndash;15:12</td>
                        <td>
                            <span class="paper-title">SwitchOut: an Efficient Data Augmentation Algorithm for Neural Machine Translation.</span>
                            <em>Xinyi Wang, Hieu Pham, Zihang Dai and Graham Neubig</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1100" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305206127" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2269">
                        <td id="paper-time">15:12&ndash;15:24</td>
                        <td>
                            <span class="paper-title">Improving Unsupervised Word-by-Word Translation with Language Model and Denoising Autoencoder.</span>
                            <em>Yunsu Kim, Jiahui Geng and Hermann Ney</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1101" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305206383" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1220">
                        <td id="paper-time">15:24&ndash;15:36</td>
                        <td>
                            <span class="paper-title">Decipherment of Substitution Ciphers with Neural Language Models.</span>
                            <em>Nishant Kambhatla, Anahita Mansouri Bigvand and Anoop Sarkar</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1102" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305206655" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2030">
                        <td id="paper-time">15:36&ndash;15:48</td>
                        <td>
                            <span class="paper-title">Rapid Adaptation of Neural Machine Translation to New Languages.</span>
                            <em>Graham Neubig and Junjie Hu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1103" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305207187" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1600">
                        <td id="paper-time">15:48&ndash;16:00</td>
                        <td>
                            <span class="paper-title">Compact Personalized Models for Neural Machine Translation.</span>
                            <em>Joern Wuebker, Patrick Simianer and John DeNero</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1104" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305207608" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-3b">
            <div id="expander"></div>
            <a href="#" class="session-title">3B: Machine Learning I</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-3b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-3b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:byron.wallace@gmail.com">Byron Wallace</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="747">
                        <td id="paper-time">15:00&ndash;15:12</td>
                        <td>
                            <span class="paper-title">Self-Governing Neural Networks for On-Device Short Text Classification.</span>
                            <em>Sujith Ravi and Zornitsa Kozareva</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1105" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305197775" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2236">
                        <td id="paper-time">15:12&ndash;15:24</td>
                        <td>
                            <span class="paper-title">Supervised Domain Enablement Attention for Personalized Domain Classification.</span>
                            <em>Joo-Kyung Kim and Young-Bum Kim</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1106" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305198062" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1039">
                        <td id="paper-time">15:24&ndash;15:36</td>
                        <td>
                            <span class="paper-title">A Deep Neural Network Sentence Level Classification Method with Context Information.</span>
                            <em>Xingyi Song, Johann Petrak and Angus Roberts</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1107" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305198319" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1198">
                        <td id="paper-time">15:36&ndash;15:48</td>
                        <td>
                            <span class="paper-title">Towards Dynamic Computation Graphs via Sparse Latent Structure.</span>
                            <em>Vlad Niculae, André F. T. Martins and Claire Cardie</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1108" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305198410" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1111">
                        <td id="paper-time">15:48&ndash;16:00</td>
                        <td>
                            <span class="paper-title">Convolutional Neural Networks with Recurrent Neural Filters.</span>
                            <em>Yi Yang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1109" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305198501" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-3c">
            <div id="expander"></div>
            <a href="#" class="session-title">3C: Semantic Parsing / Generation</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-3c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-3c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:reut.tsarfaty@gmail.com">Reut Tsarfaty</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="526">
                        <td id="paper-time">15:00&ndash;15:12</td>
                        <td>
                            <span class="paper-title">Exploiting Rich Syntactic Information for Semantic Parsing with Graph-to-Sequence Model.</span>
                            <em>Kun Xu, Lingfei Wu, Zhiguo Wang, Mo Yu, Liwei Chen and Vadim Sheinin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1110" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305213182" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1231">
                        <td id="paper-time">15:12&ndash;15:24</td>
                        <td>
                            <span class="paper-title">Retrieval-Based Neural Code Generation.</span>
                            <em>Shirley Anugrah Hayati, Raphael Olivier, Pravalika Avvaru, Pengcheng Yin, Anthony Tomasic and Graham Neubig</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1111" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305213468" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="553">
                        <td id="paper-time">15:24&ndash;15:36</td>
                        <td>
                            <span class="paper-title">SQL-to-Text Generation with Graph-to-Sequence Model.</span>
                            <em>Kun Xu, Lingfei Wu, Zhiguo Wang, Yansong Feng and Vadim Sheinin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1112" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305213739" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="739">
                        <td id="paper-time">15:36&ndash;15:48</td>
                        <td>
                            <span class="paper-title">Generating Syntactic Paraphrases.</span>
                            <em>Emilie Colin and Claire Gardent</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1113" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305214075" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1708">
                        <td id="paper-time">15:48&ndash;16:00</td>
                        <td>
                            <span class="paper-title">Neural-Davidsonian Semantic Proto-role Labeling.</span>
                            <em>Rachel Rudinger, Adam Teichert, Ryan Culkin, Sheng Zhang and Benjamin Van Durme</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1114" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305214361" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-3d">
            <div id="expander"></div>
            <a href="#" class="session-title">3D: Vision / Discourse</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-3d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-3d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:joyu@ucdavis.edu">Zhou Yu</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="626">
                        <td id="paper-time">15:00&ndash;15:12</td>
                        <td>
                            <span class="paper-title">Conversational Decision-Making Model for Predicting the King’s Decision in the Annals of the Joseon Dynasty.</span>
                            <em>JinYeong Bak and Alice Oh</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1115" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306361321" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1858">
                        <td id="paper-time">15:12&ndash;15:24</td>
                        <td>
                            <span class="paper-title">Toward Fast and Accurate Neural Discourse Segmentation.</span>
                            <em>Yizhong Wang, Sujian Li and Jingfeng Yang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1116" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306361340" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2127">
                        <td id="paper-time">15:24&ndash;15:36</td>
                        <td>
                            <span class="paper-title">A Dataset for Telling the Stories of Social Media Videos.</span>
                            <em>Spandana Gella, Mike Lewis and Marcus Rohrbach</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1117" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306361803" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1099">
                        <td id="paper-time">15:36&ndash;15:48</td>
                        <td>
                            <span class="paper-title">Cascaded Mutual Modulation for Visual Reasoning.</span>
                            <em>Yiqun Yao, Jiaming Xu, Feng Wang and Bo Xu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1118" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306362249" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="208">
                        <td id="paper-time">15:48&ndash;16:00</td>
                        <td>
                            <span class="paper-title">How agents see things: On visual representations in an emergent language game.</span>
                            <em>Diane Bouchacourt and Marco Baroni</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1119" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306362292" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-3">
            <div id="expander"></div>
            <a href="#" class="session-title">3E: Short Posters II</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Information Extraction</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="43">
                        <td>
                            <span class="poster-title">Attention-Based Capsule Networks with Dynamic Routing for Relation Extraction.</span>
                            <em>Ningyu Zhang, Shumin Deng, Zhanling Sun, Xi Chen, Wei Zhang and Huajun Chen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1120" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="159">
                        <td>
                            <span class="poster-title">Put It Back: Entity Typing with Language Model Enhancement.</span>
                            <em>Ji Xin, Hao Zhu, Xu Han, Zhiyuan Liu and Maosong Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1121" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="645">
                        <td>
                            <span class="poster-title">Event Detection with Neural Networks: A Rigorous Empirical Evaluation.</span>
                            <em>Walker Orr, Prasad Tadepalli and Xiaoli Fern</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1122" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="864">
                        <td>
                            <span class="poster-title">PubSE: A Hierarchical Model for Publication Extraction from Academic Homepages.</span>
                            <em>Yiqing Zhang, Jianzhong Qi, Rui Zhang and Chuandong Yin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1123" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1583">
                        <td>
                            <span class="poster-title">A Neural Transition-based Model for Nested Mention Recognition.</span>
                            <em>Bailin Wang, Wei Lu, Yu Wang and Hongxia Jin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1124" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1759">
                        <td>
                            <span class="poster-title">Genre Separation Network with Adversarial Training for Cross-genre Relation Extraction.</span>
                            <em>Ge Shi, Chong Feng, Lifu Huang, Boliang Zhang, Heng Ji, Lejian Liao and Heyan Huang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1125" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2143">
                        <td>
                            <span class="poster-title">Effective Use of Context in Noisy Entity Linking.</span>
                            <em>David Mueller and Greg Durrett</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1126" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2146">
                        <td>
                            <span class="poster-title">Exploiting Contextual Information via Dynamic Memory Network for Event Detection.</span>
                            <em>Shaobo Liu, Rui Cheng, Xiaoming Yu and Xueqi Cheng</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1127" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Question Answering</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="54">
                        <td>
                            <span class="poster-title">Do explanations make VQA models more predictable to a human?.</span>
                            <em>Arjun Chandrasekaran, Viraj Prabhu, Deshraj Yadav, Prithvijit Chattopadhyay and Devi Parikh</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1128" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="205">
                        <td>
                            <span class="poster-title">Facts That Matter.</span>
                            <em>Marco Ponza, Luciano Del Corro and Gerhard Weikum</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1129" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="558">
                        <td>
                            <span class="poster-title">Entity Tracking Improves Cloze-style Reading Comprehension.</span>
                            <em>Luong Hoang, Sam Wiseman and Alexander Rush</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1130" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="590">
                        <td>
                            <span class="poster-title">Adversarial Domain Adaptation for Duplicate Question Detection.</span>
                            <em>Darsh Shah, Tao Lei, Alessandro Moschitti, Salvatore Romeo and Preslav Nakov</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1131" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="663">
                        <td>
                            <span class="poster-title">Translating a Math Word Problem to a Expression Tree.</span>
                            <em>Lei Wang, Yan Wang, Deng Cai, Dongxiang Zhang and Xiaojiang Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1132" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2197">
                        <td>
                            <span class="poster-title">Semantic Linking in Convolutional Neural Networks for Answer Sentence Selection.</span>
                            <em>Massimo Nicosia and Alessandro Moschitti</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1133" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2199">
                        <td>
                            <span class="poster-title">A dataset and baselines for sequential open-domain question answering.</span>
                            <em>Ahmed Elgohary, Chen Zhao and Jordan Boyd-Graber</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1134" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Sentiment Analysis</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="22">
                        <td>
                            <span class="poster-title">Improving the results of string kernels in sentiment analysis and Arabic dialect identification by adapting them to your test set.</span>
                            <em>Radu Tudor Ionescu and Andrei M. Butnaru</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1135" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="228">
                        <td>
                            <span class="poster-title">Parameterized Convolutional Neural Networks for Aspect Level Sentiment Classification.</span>
                            <em>Binxuan Huang and Kathleen Carley</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1136" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="644">
                        <td>
                            <span class="poster-title">Improving Multi-label Emotion Classification via Sentiment Classification with Dual Attention Transfer Network.</span>
                            <em>Jianfei Yu, Luis Marujo, Jing Jiang, Pradeep Karuturi and William Brendel</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1137" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="995">
                        <td>
                            <span class="poster-title">Learning Sentiment Memories for Sentiment Modification without Parallel Data.</span>
                            <em>Yi Zhang, Jingjing Xu, Pengcheng Yang and Xu Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1138" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1117">
                        <td>
                            <span class="poster-title">Joint Aspect and Polarity Classification for Aspect-based Sentiment Analysis with End-to-End Neural Networks.</span>
                            <em>Martin Schmitt, Simon Steinheber, Konrad Schreiber and Benjamin Roth</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1139" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1797">
                        <td>
                            <span class="poster-title">Representing Social Media Users for Sarcasm Detection.</span>
                            <em>Y. Alex Kolchinski and Christopher Potts</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1140" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2326">
                        <td>
                            <span class="poster-title">Syntactical Analysis of the Weaknesses of Sentiment Analyzers.</span>
                            <em>Rohil Verma, Samuel Kim and David Walter</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1141" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Social Applications</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="586">
                        <td>
                            <span class="poster-title">Is Nike female? Exploring the role of sound symbolism in predicting brand name gender.</span>
                            <em>Sridhar Moorthy, Ruth Pogacar, Samin Khan and Yang Xu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1142" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="717">
                        <td>
                            <span class="poster-title">Improving Large-Scale Fact-Checking using Decomposable Attention Models and Lexical Tagging.</span>
                            <em>Nayeon Lee, Chien-Sheng Wu and Pascale Fung</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1143" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="814">
                        <td>
                            <span class="poster-title">Harnessing Popularity in Social Media for Extractive Summarization of Online Conversations.</span>
                            <em>Ryuji Kano, Yasuhide Miura, Motoki Taniguchi, Yan-Ying Chen, Francine Chen and Tomoko Ohkuma</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1144" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="894">
                        <td>
                            <span class="poster-title">Identifying Locus of Control in Social Media Language.</span>
                            <em>Masoud Rouhizadeh, Kokil Jaidka, Laura Smith, H. Andrew Schwartz, Anneke Buffone and Lyle Ungar</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1145" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1379">
                        <td>
                            <span class="poster-title">Somm: Into the Model.</span>
                            <em>Shengli Hu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1146" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1471">
                        <td>
                            <span class="poster-title">Fine-Grained Emotion Detection in Health-Related Online Posts.</span>
                            <em>Hamed Khanpour and Cornelia Caragea</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1147" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1522">
                        <td>
                            <span class="poster-title">The Remarkable Benefit of User-Level Aggregation for Lexical-based Population-Level Predictions.</span>
                            <em>Salvatore Giorgi, Daniel Preoţiuc-Pietro, Anneke Buffone, Daniel Rieman, Lyle Ungar and H. Andrew Schwartz</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1148" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-3">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time" title="Friday, 2 November 2018">16:00 &ndash; 16:30</span>
    </div>
    <div class="session-box" id="session-box-4">
        <div class="session-header" id="session-header-4">Long Papers &amp; Demos II (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-4a">
            <div id="expander"></div>
            <a href="#" class="session-title">4A: Language Models</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-4a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-4a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:cdyer@google.com">Chris Dyer</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="953">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">Deterministic Non-Autoregressive Neural Sequence Modeling by Iterative Refinement.</span>
                            <em>Jason Lee, Elman Mansimov and Kyunghyun Cho</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1149" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305207923" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1229">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">Large Margin Neural Language Model.</span>
                            <em>Jiaji Huang, Yi Li, Wei Ping and Liang Huang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1150" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305208380" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1799">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">Targeted Syntactic Evaluation of Language Models.</span>
                            <em>Rebecca Marvin and Tal Linzen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1151" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305208737" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2001">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">Rational Recurrences.</span>
                            <em>Hao Peng, Roy Schwartz, Sam Thomson and Noah A. Smith</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1152" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305209046" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2117">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">Efficient Contextualized Representation: Language Model Pruning for Sequence Labeling.</span>
                            <em>Liyuan Liu, Xiang Ren, Jingbo Shang, Xiaotao Gu, Jian Peng and Jiawei Han</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1153" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305209444" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-4b">
            <div id="expander"></div>
            <a href="#" class="session-title">4B: Information Extraction</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-4b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-4b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:jih@rpi.edu">Heng Ji</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="224">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">Automatic Event Salience Identification.</span>
                            <em>Zhengzhong Liu, Chenyan Xiong, Teruko Mitamura and Eduard Hovy</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1154" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305198570" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="766">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">Temporal Information Extraction by Predicting Relative Time-lines.</span>
                            <em>Artuur Leeuwenberg and Marie-Francine Moens</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1155" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305198795" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1177">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">Jointly Multiple Events Extraction via Attention-based Graph Information Aggregation.</span>
                            <em>Xiao Liu, Zhunchen Luo and Heyan Huang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1156" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305198933" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1613">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">RESIDE: Improving Distantly-Supervised Neural Relation Extraction using Side Information.</span>
                            <em>Shikhar Vashishth, Rishabh Joshi, Sai Suman Prayaga, Chiranjib Bhattacharyya and Partha Talukdar</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1157" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305199302" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1924">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">Collective Event Detection via a Hierarchical and Bias Tagging Networks with Gated Multi-level Attention Mechanisms.</span>
                            <em>Yubo Chen, Hang Yang, Kang Liu, Jun Zhao and Yantao Jia</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1158" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305199664" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-4c">
            <div id="expander"></div>
            <a href="#" class="session-title">4C: Syntactic Parsing</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-4c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-4c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:joakim.nivre@lingfil.uu.se">Joakim Nivre</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="217">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">Valency-Augmented Dependency Parsing.</span>
                            <em>Tianze Shi and Lillian Lee</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1159" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305214708" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="336">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">Unsupervised Learning of Syntactic Structure with Invertible Neural Projections.</span>
                            <em>Junxian He, Graham Neubig and Taylor Berg-Kirkpatrick</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1160" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305215139" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="791">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">Dynamic Oracles for Top-Down and In-Order Shift-Reduce Constituent Parsing.</span>
                            <em>Daniel Fernández-González and Carlos Gómez-Rodríguez</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1161" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305215645" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1147">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">Constituent Parsing as Sequence Labeling.</span>
                            <em>Carlos Gómez-Rodríguez and David Vilares</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1162" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305216237" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2217">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">Synthetic Data Made to Order: The Case of Parsing.</span>
                            <em>Dingquan Wang and Jason Eisner</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1163" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305216917" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-4d">
            <div id="expander"></div>
            <a href="#" class="session-title">4D: Visual QA</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-4d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-4d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:CarinaSilberer@gmail.com">Carina Silberer</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="247">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">Tell-and-Answer: Towards Explainable Visual Question Answering using Attributes and Captions.</span>
                            <em>Qing Li, Jianlong Fu, Dongfei Yu, Tao Mei and Jiebo Luo</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1164" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306362344" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="282">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">Learning a Policy for Opportunistic Active Learning.</span>
                            <em>Aishwarya Padmakumar, Peter Stone and Raymond Mooney</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1165" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306362379" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1213">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">RecipeQA: A Challenge Dataset for Multimodal Comprehension of Cooking Recipes.</span>
                            <em>Semih Yagcioglu, Aykut Erdem, Erkut Erdem and Nazli Ikizler-Cinbis</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1166" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306363701" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1650">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">TVQA: Localized, Compositional Video Question Answering.</span>
                            <em>Jie Lei, Licheng Yu, Mohit Bansal and Tamara Berg</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1167" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306364803" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1763">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">Localizing Moments in Video with Temporal Language.</span>
                            <em>Lisa Anne Hendricks, Oliver Wang, Eli Shechtman, Josef Sivic, Trevor Darrell and Bryan Russell</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1168" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306365884" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-4">
            <div id="expander"></div>
            <a href="#" class="session-title">4E: Semantics III (Posters and Demos)</a>
            <br/>
            <span class="session-time" title="Friday, 2 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Lexical Semantics</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="179">
                        <td>
                            <span class="poster-title">Card-660: Cambridge Rare Word Dataset - a Reliable Benchmark for Infrequent Word Representation Models.</span>
                            <em>Mohammad Taher Pilehvar, Dimitri Kartsaklis, Victor Prokhorov and Nigel Collier</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1169" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="244">
                        <td>
                            <span class="poster-title">Leveraging Gloss Knowledge in Neural Word Sense Disambiguation by Hierarchical Co-Attention.</span>
                            <em>Fuli Luo, Tianyu Liu, Zexue He, Qiaolin Xia, Zhifang Sui and Baobao Chang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1170" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="741">
                        <td>
                            <span class="poster-title">Weeding out Conventionalized Metaphors: A Corpus of Novel Metaphor Annotations.</span>
                            <em>Erik-Lân Do Dinh, Hannah Wieland and Iryna Gurevych</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1171" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="769">
                        <td>
                            <span class="poster-title">Streaming word similarity mining on the cheap.</span>
                            <em>Olof Görnerup and Daniel Gillblad</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1172" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="819">
                        <td>
                            <span class="poster-title">Memory, Show the Way: Memory Based Few Shot Word Representation Learning.</span>
                            <em>Jingyuan Sun, Shaonan Wang and Chengqing Zong</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1173" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="983">
                        <td>
                            <span class="poster-title">Disambiguated skip-gram model.</span>
                            <em>Karol Grzegorczyk and Marcin Kurdziel</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1174" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1037">
                        <td>
                            <span class="poster-title">Picking Apart Story Salads.</span>
                            <em>Su Wang, Eric Holgate, Greg Durrett and Katrin Erk</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1175" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1175">
                        <td>
                            <span class="poster-title">Dynamic Meta-Embeddings for Improved Sentence Representations.</span>
                            <em>Douwe Kiela, Changhan Wang and Kyunghyun Cho</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1176" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1257">
                        <td>
                            <span class="poster-title">A Probabilistic Model for Joint Learning of Word Embeddings from Texts and Images.</span>
                            <em>Melissa Ailem, Bowen Zhang, Aurélien Bellet, Pascal Denis and Fei Sha</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1177" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1470">
                        <td>
                            <span class="poster-title">Transfer and Multi-Task Learning for Noun–Noun Compound Interpretation.</span>
                            <em>Murhaf Fares, Stephan Oepen and Erik Velldal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1178" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1472">
                        <td>
                            <span class="poster-title">Dissecting Contextual Word Embeddings: Architecture and Representation.</span>
                            <em>Matthew Peters, Mark Neumann, Luke Zettlemoyer and Wen-tau Yih</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1179" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1790">
                        <td>
                            <span class="poster-title">Preposition Sense Disambiguation and Representation.</span>
                            <em>Hongyu Gong, Jiaqi Mu, Suma Bhat and Pramod Viswanath</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1180" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1870">
                        <td>
                            <span class="poster-title">Auto-Encoding Dictionary Definitions into Consistent Word Embeddings.</span>
                            <em>Tom Bosc and Pascal Vincent</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1181" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2221">
                        <td>
                            <span class="poster-title">Spot the Odd Man Out: Exploring the Associative Power of Lexical Resources.</span>
                            <em>Gabriel Stanovsky and Mark Hopkins</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1182" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1346-TACL">
                        <td>
                            <span class="poster-title">[TACL] Linear Algebraic Structure of Word Senses, with Applications to Polysemy.</span>
                            <em>Sanjeev Arora, Yuanzhi Li, Yingyu Liang, Tengyu Ma, Andrej Risteski</em>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Semantic Inference</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="682">
                        <td>
                            <span class="poster-title">Neural Multitask Learning for Simile Recognition.</span>
                            <em>Lizhen Liu, Xiao Hu, Wei Song, Ruiji Fu, Ting Liu and Guoping Hu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1183" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="911">
                        <td>
                            <span class="poster-title">Structured Alignment Networks for Matching Sentences.</span>
                            <em>Yang Liu, Matt Gardner and Mirella Lapata</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1184" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1669">
                        <td>
                            <span class="poster-title">Compare, Compress and Propagate: Enhancing Neural Architectures with Alignment Factorization for Natural Language Inference.</span>
                            <em>Yi Tay, Anh Tuan Luu and Siu Cheung Hui</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1185" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1821">
                        <td>
                            <span class="poster-title">Convolutional Interaction Network for Natural Language Inference.</span>
                            <em>Jingjing Gong, Xipeng Qiu, Xinchi Chen, Dong Liang and Xuanjing Huang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1186" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1837">
                        <td>
                            <span class="poster-title">Lessons from Natural Language Inference in the Clinical Domain.</span>
                            <em>Alexey Romanov and Chaitanya Shivade</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1187" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Semantic Parsing</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="264">
                        <td>
                            <span class="poster-title">Question Generation from SQL Queries Improves Neural Semantic Parsing.</span>
                            <em>Daya Guo, Yibo Sun, Duyu Tang, Nan Duan, Jian Yin, Hong Chi, James Cao, Peng Chen and Ming Zhou</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1188" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="670">
                        <td>
                            <span class="poster-title">SemRegex: A Semantics-Based Approach for Generating Regular Expressions from Natural Language Specifications.</span>
                            <em>Zexuan Zhong, Jiaqi Guo, Wei Yang, Jian Peng, Tao Xie, Jian-Guang Lou, Ting Liu and Dongmei Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1189" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="829">
                        <td>
                            <span class="poster-title">Decoupling Structure and Lexicon for Zero-Shot Semantic Parsing.</span>
                            <em>Jonathan Herzig and Jonathan Berant</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1190" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1052">
                        <td>
                            <span class="poster-title">A Span Selection Model for Semantic Role Labeling.</span>
                            <em>Hiroki Ouchi, Hiroyuki Shindo and Yuji Matsumoto</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1191" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1100">
                        <td>
                            <span class="poster-title">Mapping Language to Code in Programmatic Context.</span>
                            <em>Srinivasan Iyer, Ioannis Konstas, Alvin Cheung and Luke Zettlemoyer</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1192" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1261">
                        <td>
                            <span class="poster-title">SyntaxSQLNet: Syntax Tree Networks for Complex and Cross-Domain Text-to-SQL Task.</span>
                            <em>Tao Yu, Michihiro Yasunaga, Kai Yang, Rui Zhang, Dongxu Wang, Zifan Li and Dragomir Radev</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1193" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1398">
                        <td>
                            <span class="poster-title">Cross-lingual Decompositional Semantic Parsing.</span>
                            <em>Sheng Zhang, Xutai Ma, Rachel Rudinger, Kevin Duh and Benjamin Van Durme</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1194" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1699">
                        <td>
                            <span class="poster-title">Learning to Learn Semantic Parsers from Natural Language Supervision.</span>
                            <em>Igor Labutov, Bishan Yang and Tom Mitchell</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1195" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1766">
                        <td>
                            <span class="poster-title">DeepCx: A transition-based approach for shallow semantic parsing with complex constructional triggers.</span>
                            <em>Jesse Dunietz, Jaime Carbonell and Lori Levin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1196" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1791">
                        <td>
                            <span class="poster-title">What It Takes to Achieve 100% Condition Accuracy on WikiSQL.</span>
                            <em>Semih Yavuz, Izzeddin Gur, Yu Su and Xifeng Yan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1197" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2073">
                        <td>
                            <span class="poster-title">Better Transition-Based AMR Parsing with a Refined Search Space.</span>
                            <em>Zhijiang Guo and Wei Lu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1198" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Demos</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="8-demo">
                        <td>
                            <span class="poster-title">TRANX: A Transition-based Neural Abstract Syntax Parser for Semantic Parsing and Code Generation.</span>
                            <em>Pengcheng Yin and Graham Neubig</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2002" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="25-demo">
                        <td>
                            <span class="poster-title">Visual Interrogation of Attention-Based Models for Natural Language Inference and Machine Comprehension.</span>
                            <em>Shusen Liu, Tao Li, Zhimin Li, Vivek Srikumar, Valerio Pascucci and Peer-Timo Bremer</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2007" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="62-demo">
                        <td>
                            <span class="poster-title">Magnitude: A Fast, Efficient Universal Vector Embedding Utility Package.</span>
                            <em>Ajay Patel, Alexander Sands, Chris Callison-Burch and Marianna Apidianaki</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2021" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="77-demo">
                        <td>
                            <span class="poster-title">Universal Sentence Encoder for English.</span>
                            <em>Daniel Cer, Yinfei Yang, Sheng-yi Kong, Nan Hua, Nicole Limtiaco, Rhomni St. John, Noah Constant, Mario Guajardo-Cespedes, Steve Yuan, Chris Tar, Brian Strope and Ray Kurzweil</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2029" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="day" id="day-4">Saturday, 3 November 2018</div>
    <div class="session-box" id="session-box-5">
        <div class="session-header" id="session-header-5">Long Papers &amp; Demos III (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-5a">
            <div id="expander"></div>
            <a href="#" class="session-title">5A: Semantics IV</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-5a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-5a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:oe@ifi.uio.no">Stephan Oepen</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="654">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">Heuristically Informed Unsupervised Idiom Usage Recognition.</span>
                            <em>Changsheng Liu and Rebecca Hwa</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1199" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305931117" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="835">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">Coming to Your Senses: on Controls and Evaluation Sets in Polysemy Research.</span>
                            <em>Haim Dubossarsky, Eitan Grossman and Daphna Weinshall</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1200" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305931948" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1581">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">Predicting Semantic Relations using Global Graph Properties.</span>
                            <em>Yuval Pinter and Jacob Eisenstein</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1201" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305933339" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1728">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">Learning Scalar Adjective Intensity from Paraphrases.</span>
                            <em>Anne Cocos, Veronica Wharton, Ellie Pavlick, Marianna Apidianaki and Chris Callison-Burch</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1202" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305934622" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2009">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">Pointwise HSIC: A Linear-Time Kernelized Co-occurrence Norm for Sparse Linguistic Expressions.</span>
                            <em>Sho Yokoi, Sosuke Kobayashi, Kenji Fukumizu, Jun Suzuki and Kentaro Inui</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1203" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305935544" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-5b">
            <div id="expander"></div>
            <a href="#" class="session-title">5B: Summarization</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-5b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-5b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:feiliu@cs.ucf.edu">Fei Liu</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="469">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">Neural Related Work Summarization with a Joint Context-driven Attention Mechanism.</span>
                            <em>Yongzhen Wang, Xiaozhong Liu and Zheng Gao</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1204" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305686976" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="731">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">Improving Neural Abstractive Document Summarization with Explicit Information Selection Modeling.</span>
                            <em>Wei Li, Xinyan Xiao, Yajuan Lyu and Yuanzhuo Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1205" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305885506" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1090">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">Don't Give Me the Details, Just the Summary! Topic-Aware Convolutional Neural Networks for Extreme Summarization.</span>
                            <em>Shashi Narayan, Shay B. Cohen and Mirella Lapata</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1206" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305885893" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1778">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">Improving Abstraction in Text Summarization.</span>
                            <em>Wojciech Kryściński, Romain Paulus, Caiming Xiong and Richard Socher</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1207" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305886179" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2164">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">Content Selection in Deep Learning Models of Summarization.</span>
                            <em>Chris Kedzie, Kathleen McKeown and Hal Daume III</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1208" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305886331" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-5c">
            <div id="expander"></div>
            <a href="#" class="session-title">5C: IR / Text Mining</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-5c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-5c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:amoschitti@gmail.com">Alessandro Moschitti</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="190">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">Improved Semantic-Aware Network Embedding with Fine-Grained Word Alignment.</span>
                            <em>Dinghan Shen, Xinyuan Zhang, Ricardo Henao and Lawrence Carin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1209" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306030030" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="391">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">Learning Context-Sensitive Convolutional Filters for Text Processing.</span>
                            <em>Dinghan Shen, Martin Renqiang Min, Yitong Li and Lawrence Carin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1210" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306040551" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1186">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">Deep Relevance Ranking Using Enhanced Document-Query Interactions.</span>
                            <em>Ryan McDonald, George Brokos and Ion Androutsopoulos</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1211" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306041612" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1586">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">Learning Neural Representation for CLIR with Adversarial Framework.</span>
                            <em>Bo Li and Ping Cheng</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1212" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306042980" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1659">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">AD3: Attentive Deep Document Dater.</span>
                            <em>Swayambhu Nath Ray, Shib Sankar Dasgupta and Partha Talukdar</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1213" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306043956" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-5d">
            <div id="expander"></div>
            <a href="#" class="session-title">5D: Machine Learning II</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-5d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-5d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:kw@kwchang.net">Kai-Wei Chang</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1406">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">Gromov-Wasserstein Alignment of Word Embedding Spaces.</span>
                            <em>David Alvarez-Melis and Tommi Jaakkola</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1214" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305660461" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1504">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">Deep Probabilistic Logic: A Unifying Framework for Indirect Supervision.</span>
                            <em>Hai Wang and Hoifung Poon</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1215" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305661315" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1621">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">Deriving Machine Attention from Human Rationales.</span>
                            <em>Yujia Bao, Shiyu Chang, Mo Yu and Regina Barzilay</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1216" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305661928" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1741">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">Semi-Supervised Sequence Modeling with Cross-View Training.</span>
                            <em>Kevin Clark, Minh-Thang Luong, Christopher D. Manning and Quoc Le</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1217" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305662403" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1430-TACL">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">[TACL] Comparing Bayesian Models of Annotation.</span>
                            <em>Silviu Paun, Bob Carpenter, Jon Chamberlain, Dirk Hovy, Udo Kruschwitz, Massimo Poesio</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="/downloads/tacl-papers/EMNLP-TACL01.pdf" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305663095" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-5">
            <div id="expander"></div>
            <a href="#" class="session-title">5E: Information Extraction, Question Answering (Posters and Demos)</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Entities and Coreference</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="171">
                        <td>
                            <span class="poster-title">Mapping Text to Knowledge Graph Entities using Multi-Sense LSTMs.</span>
                            <em>Dimitri Kartsaklis, Mohammad Taher Pilehvar and Nigel Collier</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1221" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="415">
                        <td>
                            <span class="poster-title">Differentiating Concepts and Instances for Knowledge Graph Embedding.</span>
                            <em>Xin Lv, Lei Hou, Juanzi Li and Zhiyuan Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1222" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1234">
                        <td>
                            <span class="poster-title">One-Shot Relational Learning for Knowledge Graphs.</span>
                            <em>Wenhan Xiong, Mo Yu, Shiyu Chang, Xiaoxiao Guo and William Yang Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1223" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1762">
                        <td>
                            <span class="poster-title">Regular Expression Guided Entity Mention Mining from Noisy Web Data.</span>
                            <em>Shanshan Zhang, Lihong He, Slobodan Vucetic and Eduard Dragut</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1224" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="575">
                        <td>
                            <span class="poster-title">A Deterministic Algorithm for Bridging Anaphora Resolution.</span>
                            <em>Yufang Hou</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1219" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1104">
                        <td>
                            <span class="poster-title">A Knowledge Hunting Framework for Common Sense Reasoning.</span>
                            <em>Ali Emami, Noelia De La Cruz, Adam Trischler, Kaheer Suleman and Jackie Chi Kit Cheung</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1220" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="615">
                        <td>
                            <span class="poster-title">Neural Adaptation Layers for Cross-domain Named Entity Recognition.</span>
                            <em>Bill Yuchen Lin and Wei Lu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1226" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="855">
                        <td>
                            <span class="poster-title">Entity Linking within a Social Media Platform: A Case Study on Yelp.</span>
                            <em>Hongliang Dai, Yangqiu Song, Liwei Qiu and Rijia Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1227" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1094">
                        <td>
                            <span class="poster-title">Annotation of a Large Clinical Entity Corpus.</span>
                            <em>Pinal Patel, Disha Davey, Vishal Panchal and Parth Pathak</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1228" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1344">
                        <td>
                            <span class="poster-title">Visual Supervision in Bootstrapped Information Extraction.</span>
                            <em>Matthew Berger, Ajay Nagesh, Joshua Levine, Mihai Surdeanu and Helen Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1229" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1631">
                        <td>
                            <span class="poster-title">Learning Named Entity Tagger using Domain-Specific Dictionary.</span>
                            <em>Jingbo Shang, Liyuan Liu, Xiaotao Gu, Xiang Ren, Teng Ren and Jiawei Han</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1230" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1973">
                        <td>
                            <span class="poster-title">Zero-Shot Open Entity Typing as Type-Compatible Grounding.</span>
                            <em>Ben Zhou, Daniel Khashabi, Chen-Tse Tsai and Dan Roth</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1231" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Question Answering and Reading Comprehension</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="94">
                        <td>
                            <span class="poster-title">Attention-Guided Answer Distillation for Machine Reading Comprehension.</span>
                            <em>Minghao Hu, Yuxing Peng, Furu Wei, Zhen Huang, Dongsheng Li, Nan Yang and Ming Zhou</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1232" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="534">
                        <td>
                            <span class="poster-title">Interpretation of Natural Language Rules in Conversational Machine Reading.</span>
                            <em>Marzieh Saeidi, Max Bartolo, Patrick Lewis, Sameer Singh, Tim Rocktäschel, Mike Sheldon, Guillaume Bouchard and Sebastian Riedel</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1233" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="771">
                        <td>
                            <span class="poster-title">A State-transition Framework to Answer Complex Questions over Knowledge Base.</span>
                            <em>Sen Hu, Lei Zou and Xinbo Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1234" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="833">
                        <td>
                            <span class="poster-title">A Multi-answer Multi-task Framework for Real-world Machine Reading Comprehension.</span>
                            <em>Jiahua Liu, Wan Wei, Maosong Sun, Hao Chen, Yantao Du and Dekang Lin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1235" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1110">
                        <td>
                            <span class="poster-title">Logician and Orator: Learning from the Duality between Language and Knowledge in Open Domain.</span>
                            <em>Mingming Sun, Xu Li and Ping Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1236" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1630">
                        <td>
                            <span class="poster-title">MemoReader: Large-Scale Reading Comprehension through Neural Memory Controller.</span>
                            <em>Seohyun Back, Seunghak Yu, Sathish Reddy Indurthi, Jihie Kim and Jaegul Choo</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1237" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1677">
                        <td>
                            <span class="poster-title">Multi-Granular Sequence Encoding via Dilated Compositional Units for Reading Comprehension.</span>
                            <em>Yi Tay, Anh Tuan Luu and Siu Cheung Hui</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1238" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1721">
                        <td>
                            <span class="poster-title">Neural Compositional Denotational Semantics for Question Answering.</span>
                            <em>Nitish Gupta and Mike Lewis</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1239" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2168">
                        <td>
                            <span class="poster-title">Cross-Pair Text Representations for Answer Sentence Selection.</span>
                            <em>Kateryna Tymoshenko and Alessandro Moschitti</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1240" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2177">
                        <td>
                            <span class="poster-title">QuAC: Question Answering in Context.</span>
                            <em>Eunsol Choi, He He, Mohit Iyyer, Mark Yatskar, Wen-tau Yih, Yejin Choi, Percy Liang and Luke Zettlemoyer</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1241" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2244">
                        <td>
                            <span class="poster-title">Knowledge Base Question Answering via Encoding of Complex Query Graphs.</span>
                            <em>Kangqi Luo, Fengli Lin, Xusheng Luo and Kenny Zhu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1242" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Relation Extraction</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="58">
                        <td>
                            <span class="poster-title">Neural Relation Extraction via Inner-Sentence Noise Reduction and Transfer Learning.</span>
                            <em>Tianyi Liu, Xinsong Zhang, Wanhao Zhou and Weijia Jia</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1243" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="297">
                        <td>
                            <span class="poster-title">Graph Convolution over Pruned Dependency Trees Improves Relation Extraction.</span>
                            <em>Yuhao Zhang, Peng Qi and Christopher D. Manning</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1244" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="425">
                        <td>
                            <span class="poster-title">Multi-Level Structured Self-Attentions for Distantly Supervised Relation Extraction.</span>
                            <em>Jinhua Du, Jingguang Han, Andy Way and Dadong Wan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1245" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="712">
                        <td>
                            <span class="poster-title">N-ary Relation Extraction using Graph-State LSTM.</span>
                            <em>Linfeng Song, Yue Zhang, Zhiguo Wang and Daniel Gildea</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1246" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1009">
                        <td>
                            <span class="poster-title">Hierarchical Relation Extraction with Coarse-to-Fine Grained Attention.</span>
                            <em>Xu Han, Pengfei Yu, Zhiyuan Liu, Maosong Sun and Peng Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1247" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1020">
                        <td>
                            <span class="poster-title">Label-Free Distant Supervision for Relation Extraction via Knowledge Graph Embedding.</span>
                            <em>Guanying Wang, Wen Zhang, Ruoxu Wang, Yalin Zhou, Xi Chen, Wei Zhang, Hai Zhu and Huajun Chen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1248" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1048">
                        <td>
                            <span class="poster-title">Extracting Entities and Relations with Joint Minimum Risk Training.</span>
                            <em>Changzhi Sun, Yuanbin Wu, Man Lan, Shiliang Sun, Wenting Wang, Kuang-Chih Lee and Kewen Wu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1249" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1232">
                        <td>
                            <span class="poster-title">Large-scale Exploration of Neural Relation Classification Architectures.</span>
                            <em>Hoang-Quynh Le, Duy-Cat Can, Sinh T. Vu, Thanh Hai Dang, Mohammad Taher Pilehvar and Nigel Collier</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1250" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1751">
                        <td>
                            <span class="poster-title">Possessors Change Over Time: A Case Study with Artworks.</span>
                            <em>Dhivya Chinnappa and Eduardo Blanco</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1251" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Demos</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="39-demo">
                        <td>
                            <span class="poster-title">CogCompTime: A Tool for Understanding Time in Natural Language.</span>
                            <em>Qiang Ning, Ben Zhou, Zhili Feng, Haoruo Peng and Dan Roth</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2013" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="29-demo">
                        <td>
                            <span class="poster-title">DERE: A Task and Domain-Independent Slot Filling Framework for Declarative Relation Extraction.</span>
                            <em>Heike Adel, Laura Ana Maria Bostan, Sean Papay, Sebastian Padó and Roman Klinger</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2008" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="63-demo">
                        <td>
                            <span class="poster-title">Integrating Knowledge-Supported Search into the INCEpTION Annotation Platform.</span>
                            <em>Beto Boullosa, Richard Eckart de Castilho, Naveen Kumar, Jan-Christoph Klie and Iryna Gurevych</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2022" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="67-demo">
                        <td>
                            <span class="poster-title">OpenKE: An Open Toolkit for Knowledge Embedding.</span>
                            <em>Xu Han, Shulin Cao, Xin Lv, Yankai Lin, Zhiyuan Liu, Maosong Sun and Juanzi Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2024" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="21-demo">
                        <td>
                            <span class="poster-title">An Interactive Web-Interface for Visualizing the Inner Workings of the Question Answering LSTM.</span>
                            <em>Ekaterina Loginova and Günter Neumann</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2006" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="58-demo">
                        <td>
                            <span class="poster-title">An Interface for Annotating Science Questions.</span>
                            <em>Michael Boratko, Harshit Padigela, Divyendra Mikkilineni, Pritish Yuvraj, Rajarshi Das, Andrew McCallum, Maria Chang, Achille Fokoue, Pavan Kapanipathi, Nicholas Mattei, Ryan Musa, Kartik Talamadupula and Michael Witbrock</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2018" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="61-demo">
                        <td>
                            <span class="poster-title">Interactive Instance-based Evaluation of Knowledge Base Question Answering.</span>
                            <em>Daniil Sorokin and Iryna Gurevych</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2020" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-4">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time" title="Saturday, 3 November 2018">10:30 &ndash; 11:00</span>
    </div>
    <div class="session-box" id="session-box-6">
        <div class="session-header" id="session-header-6">Long Papers &amp; Demos IV (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-6a">
            <div id="expander"></div>
            <a href="#" class="session-title">6A: Dialogue I</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-6a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-6a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:mbansal@cs.unc.edu">Mohit Bansal</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="582">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">Using Lexical Alignment and Referring Ability to Address Data Sparsity in Situated Dialog Reference Resolution.</span>
                            <em>Todd Shore and Gabriel Skantze</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1252" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305936322" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1612">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">Subgoal Discovery for Hierarchical Dialogue Policy Learning.</span>
                            <em>Da Tang, Xiujun Li, Jianfeng Gao, Chong Wang, Lihong Li and Tony Jebara</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1253" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305937184" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1652">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">Supervised Clustering of Questions into Intents for Dialog System Applications.</span>
                            <em>Iryna Haponchyk, Antonio Uva, Seunghak Yu, Olga Uryupina and Alessandro Moschitti</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1254" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305938531" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2005">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Towards Exploiting Background Knowledge for Building Conversation Systems.</span>
                            <em>Nikita Moghe, Siddhartha Arora, Suman Banerjee and Mitesh M. Khapra</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1255" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305939688" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2300">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Decoupling Strategy and Generation in Negotiation Dialogues.</span>
                            <em>He He, Derek Chen, Anusha Balakrishnan and Percy Liang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1256" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305940786" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-6b">
            <div id="expander"></div>
            <a href="#" class="session-title">6B: Question Answering II</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-6b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-6b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:william@cs.ucsb.edu">William Wang</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="628">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">Large-scale Cloze Test Dataset Created by Teachers.</span>
                            <em>Qizhe Xie, Guokun Lai, Zihang Dai and Eduard Hovy</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1257" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305886563" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1849">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">emrQA: A Large Corpus for Question Answering on Electronic Medical Records.</span>
                            <em>Anusri Pampari, Preethi Raghavan, Jennifer Liang and Jian Peng</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1258" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305887077" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2015">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering.</span>
                            <em>Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William Cohen, Ruslan Salakhutdinov and Christopher D. Manning</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1259" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305887533" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2133">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Can a Suit of Armor Conduct Electricity? A New Dataset for Open Book Question Answering.</span>
                            <em>Todor Mihaylov, Peter Clark, Tushar Khot and Ashish Sabharwal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1260" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305887978" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2312">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Evaluating Theory of Mind in Question Answering.</span>
                            <em>Aida Nematzadeh, Kaylee Burns, Erin Grant, Alison Gopnik and Tom Griffiths</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1261" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305888739" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-6c">
            <div id="expander"></div>
            <a href="#" class="session-title">6C: Semantics V</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-6c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-6c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:iv250@cam.ac.uk">Ivan Vulić</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1128">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">A Unified Syntax-aware Framework for Semantic Role Labeling.</span>
                            <em>Zuchao Li, Shexia He, Jiaxun Cai, Zhuosheng Zhang, Hai Zhao, Gongshen Liu, Linlin Li and Luo Si</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1262" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306044975" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1247">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">Semantics as a Foreign Language.</span>
                            <em>Gabriel Stanovsky and Ido Dagan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1263" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306045906" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1478">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">An AMR Aligner Tuned by Transition-based Parser.</span>
                            <em>Yijia Liu, Wanxiang Che, Bo Zheng, Bing Qin and Ting Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1264" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306049123" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2179">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Dependency-based Hybrid Trees for Semantic Parsing.</span>
                            <em>Zhanming Jie and Wei Lu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1265" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306052219" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2214">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Policy Shaping and Generalized Update Equations for Semantic Parsing from Denotations.</span>
                            <em>Dipendra Misra, Ming-Wei Chang, Xiaodong He and Wen-tau Yih</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1266" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306053202" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-6d">
            <div id="expander"></div>
            <a href="#" class="session-title">6D: Multilingual Methods II</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-6d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-6d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:bplank@gmail.com">Barbara Plank</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="189">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">Sentence Compression for Arbitrary Languages via Multilingual Pivoting.</span>
                            <em>Jonathan Mallinson, Rico Sennrich and Mirella Lapata</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1267" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305663630" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="768">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">Unsupervised Cross-lingual Transfer of Word Embedding Spaces.</span>
                            <em>Ruochen Xu, Yiming Yang, Naoki Otani and Yuexin Wu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1268" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305664457" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1605">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">XNLI: Evaluating Cross-lingual Sentence Representations.</span>
                            <em>Alexis Conneau, Ruty Rinott, Guillaume Lample, Adina Williams, Samuel Bowman, Holger Schwenk and Veselin Stoyanov</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1269" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305665271" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1880">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Joint Multilingual Supervision for Cross-lingual Entity Linking.</span>
                            <em>Shyam Upadhyay, Nitish Gupta and Dan Roth</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1270" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305666173" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2249">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Fine-grained Coordinated Cross-lingual Text Stream Alignment for Endless Language Knowledge Acquisition.</span>
                            <em>Tao Ge, Qing Dou, Heng Ji, Lei Cui, Baobao Chang, Zhifang Sui, Furu Wei and Ming Zhou</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1271" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305667349" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-6">
            <div id="expander"></div>
            <a href="#" class="session-title">6E: Syntax, Morphology, Vision &amp; Language I (Posters and Demos)</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Morphology, Word Segmentation and POS Tagging</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="42">
                        <td>
                            <span class="poster-title">Sanskrit Word Segmentation Using Character-level Recurrent and Convolutional Neural Networks.</span>
                            <em>Oliver Hellwig and Sebastian Nehrdich</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1295" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1446-TACL">
                        <td>
                            <span class="poster-title">[TACL] Universal Word Segmentation: Implementation and Interpretation.</span>
                            <em>Yan Shao, Christian Hardmeier, Joakim Nivre</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="/downloads/tacl-papers/EMNLP-TACL02.pdf" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="701">
                        <td>
                            <span class="poster-title">WECA：A WordNet-Encoded Collocation-Attention Network for Homographic Pun Recognition.</span>
                            <em>Yufeng Diao, Hongfei Lin, Di Wu, Liang Yang, Kan Xu, Zhihao Yang, Jian Wang, Shaowu Zhang, Bo Xu and Dongyu Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1272" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="928">
                        <td>
                            <span class="poster-title">A Hybrid Approach to Automatic Corpus Generation for Chinese Spelling Check.</span>
                            <em>Dingmin Wang, Yan Song, Jing Li, Jialong Han and Haisong Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1273" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="622">
                        <td>
                            <span class="poster-title">Transferring from Formal Newswire Domain with Hypernet for Twitter POS Tagging.</span>
                            <em>Tao Gui, Qi Zhang, Jingjing Gong, Minlong Peng, di liang, Keyu Ding and Xuanjing Huang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1275" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1080">
                        <td>
                            <span class="poster-title">Free as in Free Word Order: An Energy Based Model for Word Segmentation and Morphological Tagging in Sanskrit.</span>
                            <em>Amrith Krishna, Bishal Santra, Sasi Prasanth Bandaru, Gaurav Sahu, Vishnu Dutt Sharma, Pavankumar Satuluri and Pawan Goyal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1276" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1174">
                        <td>
                            <span class="poster-title">A Challenge Set and Methods for Noun-Verb Ambiguity.</span>
                            <em>Ali Elkahky, Kellie Webster, Daniel Andor and Emily Pitler</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1277" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1237">
                        <td>
                            <span class="poster-title">What do character-level models learn about morphology? The case of dependency parsing.</span>
                            <em>Clara Vania, Andreas Grivas and Adam Lopez</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1278" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2208">
                        <td>
                            <span class="poster-title">Learning Better Internal Structure of Words for Sequence Labeling.</span>
                            <em>Yingwei Xin, Ethan Hart, Vibhuti Mahajan and Jean David Ruvini</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1279" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Vision and Language</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="761">
                        <td>
                            <span class="poster-title">ICON: Interactive Conversational Memory Network for Multimodal Emotion Detection.</span>
                            <em>Devamanyu Hazarika, Soujanya Poria, Rada Mihalcea, Erik Cambria and Roger Zimmermann</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1280" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="978">
                        <td>
                            <span class="poster-title">Discriminative Learning of Open-Vocabulary Object Retrieval and Localization by Negative Phrase Augmentation.</span>
                            <em>Ryota Hinami and Shin'ichi Satoh</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1281" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1744">
                        <td>
                            <span class="poster-title">Grounding Semantic Roles in Images.</span>
                            <em>Carina Silberer and Manfred Pinkal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1282" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1822">
                        <td>
                            <span class="poster-title">Commonsense Justification for Action Explanation.</span>
                            <em>Shaohua Yang, Qiaozi Gao, Sari Sadiya and Joyce Chai</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1283" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1928">
                        <td>
                            <span class="poster-title">Learning Personas from Dialogue with Attentive Memory Networks.</span>
                            <em>Eric Chu, Prashanth Vijayaraghavan and Deb Roy</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1284" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1951">
                        <td>
                            <span class="poster-title">Grounding language acquisition by training semantic parsers using captioned videos.</span>
                            <em>Candace Ross, Andrei Barbu, Yevgeni Berzak, Battushig Myanganbayar and Boris Katz</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1285" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1998">
                        <td>
                            <span class="poster-title">Translating Navigation Instructions in Natural Language to a High-Level Plan for Behavioral Robot Navigation.</span>
                            <em>Xiaoxue Zang, Ashwini Pokle, Marynel Vázquez, Kevin Chen, Juan Carlos Niebles, Alvaro Soto and Silvio Savarese</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1286" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2067">
                        <td>
                            <span class="poster-title">Mapping Instructions to Actions in 3D Environments with Visual Goal Prediction.</span>
                            <em>Dipendra Misra, Andrew Bennett, Valts Blukis, Eyvind Niklasson, Max Shatkhin and Yoav Artzi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1287" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Syntax</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="225">
                        <td>
                            <span class="poster-title">Deconvolutional Time Series Regression: A Technique for Modeling Temporally Diffuse Effects.</span>
                            <em>Cory Shain and William Schuler</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1288" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="525">
                        <td>
                            <span class="poster-title">Is this Sentence Difficult? Do you Agree?.</span>
                            <em>Dominique Brunato, Lorenzo De Mattei, Felice Dell'Orletta, Benedetta Iavarone and Giulia Venturi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1289" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="102">
                        <td>
                            <span class="poster-title">Neural Transition Based Parsing of Web Queries: An Entity Based Approach.</span>
                            <em>Rivka Malca and Roi Reichart</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1290" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="473">
                        <td>
                            <span class="poster-title">An Investigation of the Interactions Between Pre-Trained Word Embeddings, Character Models and POS Tags in Dependency Parsing.</span>
                            <em>Aaron Smith, Miryam de Lhoneux, Sara Stymne and Joakim Nivre</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1291" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1611">
                        <td>
                            <span class="poster-title">Depth-bounding is effective: Improvements and evaluation of unsupervised PCFG induction.</span>
                            <em>Lifeng Jin, Finale Doshi-Velez, Timothy Miller, William Schuler and Lane Schwartz</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1292" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1199-TACL">
                        <td>
                            <span class="poster-title">[TACL] In-Order Transition-based Constituent Parsing.</span>
                            <em>Jiangming Liu and Yue Zhang</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1425-TACL">
                        <td>
                            <span class="poster-title">[TACL] Surface Statistics of an Unknown Language Indicate How to Parse It.</span>
                            <em>Dingquan Wang and Jason Eisner</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="/downloads/tacl-papers/EMNLP-TACL06.pdf" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1745">
                        <td>
                            <span class="poster-title">Incremental Computation of Infix Probabilities for Probabilistic Finite Automata.</span>
                            <em>Marco Cognetta, Yo-Sub Han and Soon Chan Kwon</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1293" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2140">
                        <td>
                            <span class="poster-title">Syntax Encoding with Application in Authorship Attribution.</span>
                            <em>Richong Zhang, Zhiyuan Hu, Hongyu Guo and Yongyi Mao</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1294" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2076">
                        <td>
                            <span class="poster-title">Neural Quality Estimation of Grammatical Error Correction.</span>
                            <em>Shamil Chollampatt and Hwee Tou Ng</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1274" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Demos</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="18-demo">
                        <td>
                            <span class="poster-title">MorAz: an Open-source Morphological Analyzer for Azerbaijani Turkish.</span>
                            <em>Berke Özenç, Razieh Ehsani and Ercan Solak</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2005" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="33-demo">
                        <td>
                            <span class="poster-title">Juman++: A Morphological Analysis Toolkit for Scriptio Continua.</span>
                            <em>Arseny Tolmachev, Daisuke Kawahara and Sadao Kurohashi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2010" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-4">
        <span class="session-title">Lunch</span>
        <br/>
        <span class="session-time" title="Saturday, 3 November 2018">12:30 &ndash; 13:45</span>
    </div>
    <div class="session-box" id="session-box-7">
        <div class="session-header" id="session-header-7">Short Papers III (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-7a">
            <div id="expander"></div>
            <a href="#" class="session-title">7A: Dialogue II</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-7a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-7a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:zkozareva@gmail.com">Zornitsa Kozareva</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1236">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">Session-level Language Modeling for Conversational Speech.</span>
                            <em>Wayne Xiong, Lingfeng Wu, Jun Zhang and Andreas Stolcke</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1296" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305942129" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="867">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Towards Less Generic Responses in Neural Conversation Models: A Statistical Re-weighting Method.</span>
                            <em>Yahui Liu, Wei Bi, Jun Gao, Xiaojiang Liu, Jian Yao and Shuming Shi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1297" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305942945" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1309">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">Training Millions of Personalized Dialogue Agents.</span>
                            <em>Pierre-Emmanuel Mazare, Samuel Humeau, Martin Raison and Antoine Bordes</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1298" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305943582" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2226">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Towards Universal Dialogue State Tracking.</span>
                            <em>Liliang Ren, Kaige Xie, Lu Chen and Kai Yu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1299" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305944406" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1854">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">Semantic Parsing for Task Oriented Dialog using Hierarchical Representations.</span>
                            <em>Sonal Gupta, Rushin Shah, Mrinal Mohit, Anuj Kumar and Mike Lewis</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1300" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305945055" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-7b">
            <div id="expander"></div>
            <a href="#" class="session-title">7B: Social Applications II</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-7b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-7b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:shomir@psu.edu">Shomir Wilson</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1733">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">The glass ceiling in NLP.</span>
                            <em>Natalie Schluter</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1301" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305889955" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="604">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Reducing Gender Bias in Abusive Language Detection.</span>
                            <em>Ji Ho Park, Jamin Shin and Pascale Fung</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1302" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305891047" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="66">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">SafeCity: Understanding Diverse Forms of Sexual Harassment Personal Stories.</span>
                            <em>Sweta Karlekar and Mohit Bansal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1303" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305891772" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="539">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Learning multiview embeddings for assessing dementia.</span>
                            <em>Chloé Pou-Prom and Frank Rudzicz</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1304" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305892345" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1441">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">WikiConv: A Corpus of the Complete Conversational History of a Large Online Collaborative Community.</span>
                            <em>Yiqing Hua, Cristian Danescu-Niculescu-Mizil, Dario Taraborelli, Nithum Thain, Jeffery Sorensen and Lucas Dixon</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1305" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305892676" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-7c">
            <div id="expander"></div>
            <a href="#" class="session-title">7C: NER</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-7c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-7c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:ritter.1492@osu.edu">Alan Ritter</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1776">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">Marginal Likelihood Training of BiLSTM-CRF for Biomedical Named Entity Recognition from Disjoint Label Sets.</span>
                            <em>Nathan Greenberg, Trapit Bansal, Patrick Verga and Andrew McCallum</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1306" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306054703" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="146">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Adversarial training for multi-context joint entity and relation extraction.</span>
                            <em>Giannis Bekoulis, Johannes Deleu, Thomas Demeester and Chris Develder</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1307" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306055549" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="430">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">Structured Multi-Label Biomedical Text Tagging via Attentive Neural Tree Decoding.</span>
                            <em>Gaurav Singh, James Thomas, Iain Marshall, John Shawe-Taylor and Byron C. Wallace</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1308" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306056257" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2264">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Deep Exhaustive Model for Nested Named Entity Recognition.</span>
                            <em>Mohammad Golam Sohrab and Makoto Miwa</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1309" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306057139" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1518">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">Evaluating the Utility of Hand-crafted Features in Sequence Labelling.</span>
                            <em>Minghao Wu, Fei Liu and Trevor Cohn</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1310" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306112516" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-7d">
            <div id="expander"></div>
            <a href="#" class="session-title">7D: Morphology / Parsing</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-7d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-7d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:kann@nyu.edu">Katharina Kann</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="990">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">Improved Dependency Parsing using Implicit Word Connections Learned from Unlabeled Data.</span>
                            <em>Wenhui Wang, Baobao Chang and Mairgup Mansur</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1311" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305667813" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="774">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">A Framework for Understanding the Role of Morphology in Universal Dependency Parsing.</span>
                            <em>Mathieu Dehouck and Pascal Denis</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1312" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305925065" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1002">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">The Lazy Encoder: A Fine-Grained Analysis of the Role of Morphology in Neural Machine Translation.</span>
                            <em>Arianna Bisazza and Clara Tump</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1313" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305670159" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1161">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Imitation Learning for Neural Morphological String Transduction.</span>
                            <em>Peter Makarov and Simon Clematide</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1314" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305671668" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1673">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">An Encoder-Decoder Approach to the Paradigm Cell Filling Problem.</span>
                            <em>Miikka Silfverberg and Mans Hulden</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1315" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305674091" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-7">
            <div id="expander"></div>
            <a href="#" class="session-title">7E: Short Posters III</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Neural Architectures and Language Models</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="281">
                        <td>
                            <span class="poster-title">Generating Natural Language Adversarial Examples.</span>
                            <em>Moustafa Alzantot, Yash Sharma, Ahmed Elgohary, Bo-Jhang Ho, Mani Srivastava and Kai-Wei Chang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1316" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1024">
                        <td>
                            <span class="poster-title">Multi-Head Attention with Disagreement Regularization.</span>
                            <em>Jian Li, Zhaopeng Tu, Baosong Yang, Michael R. Lyu and Tong Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1317" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1731">
                        <td>
                            <span class="poster-title">Deep Bayesian Active Learning for Natural Language Processing: Results of a Large-Scale Empirical Study.</span>
                            <em>Aditya Siddhant and Zachary C. Lipton</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1318" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2149">
                        <td>
                            <span class="poster-title">Bayesian Compression for Natural Language Processing.</span>
                            <em>Nadezhda Chirkova, Ekaterina Lobacheva and Dmitry Vetrov</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1319" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="601">
                        <td>
                            <span class="poster-title">Multimodal neural pronunciation modeling for spoken languages with logographic origin.</span>
                            <em>Minh Nguyen, Gia H Ngo and Nancy Chen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1320" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2045">
                        <td>
                            <span class="poster-title">Chinese Pinyin Aided IME, Input What You Have Not Keystroked Yet.</span>
                            <em>Yafang Huang and Hai Zhao</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1321" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="722">
                        <td>
                            <span class="poster-title">Estimating Marginal Probabilities of n-grams for Recurrent Neural Language Models.</span>
                            <em>Thanapon Noraset, Doug Downey and Lidong Bing</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1322" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1393">
                        <td>
                            <span class="poster-title">How to represent a word and predict it, too: Improving tied architectures for language modelling.</span>
                            <em>Kristina Gulordava, Laura Aina and Gemma Boleda</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1323" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1516">
                        <td>
                            <span class="poster-title">The Importance of Generation Order in Language Modeling.</span>
                            <em>Nicolas Ford, Daniel Duckworth, Mohammad Norouzi and George Dahl</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1324" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Machine Translation</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="183">
                        <td>
                            <span class="poster-title">Document-Level Neural Machine Translation with Hierarchical Attention Networks.</span>
                            <em>Lesly Miculicich, Dhananjay Ram, Nikolaos Pappas and James Henderson</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1325" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="465">
                        <td>
                            <span class="poster-title">Three Strategies to Improve One-to-Many Multilingual Translation.</span>
                            <em>Yining Wang, Jiajun Zhang, Feifei Zhai, Jingfang Xu and Chengqing Zong</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1326" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="614">
                        <td>
                            <span class="poster-title">Multi-Source Syntactic Neural Machine Translation.</span>
                            <em>Anna Currey and Kenneth Heafield</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1327" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="905">
                        <td>
                            <span class="poster-title">Fixing Translation Divergences in Parallel Corpora for Neural MT.</span>
                            <em>Minh Quang Pham, Josep Crego, Jean Senellart and François Yvon</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1328" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1041">
                        <td>
                            <span class="poster-title">Adversarial Evaluation of Multimodal Machine Translation.</span>
                            <em>Desmond Elliott</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1329" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1124">
                        <td>
                            <span class="poster-title">Loss in Translation: Learning Bilingual Word Mapping with a Retrieval Criterion.</span>
                            <em>Armand Joulin, Piotr Bojanowski, Tomas Mikolov, Hervé Jégou and Edouard Grave</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1330" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1248">
                        <td>
                            <span class="poster-title">Learning When to Concentrate or Divert Attention: Self-Adaptive Attention Temperature for Neural Machine Translation.</span>
                            <em>Junyang Lin, Xu Sun, Xuancheng Ren, Muyu Li and Qi Su</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1331" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1351">
                        <td>
                            <span class="poster-title">Accelerating Asynchronous Stochastic Gradient Descent for Neural Machine Translation.</span>
                            <em>Nikolay Bogoychev, Kenneth Heafield, Alham Fikri Aji and Marcin Junczys-Dowmunt</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1332" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1355">
                        <td>
                            <span class="poster-title">Learning to Jointly Translate and Predict Dropped Pronouns with a Shared Reconstruction Mechanism.</span>
                            <em>Longyue Wang, Zhaopeng Tu, Andy Way and Qun Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1333" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1367">
                        <td>
                            <span class="poster-title">Getting Gender Right in Neural Machine Translation.</span>
                            <em>Eva Vanmassenhove, Christian Hardmeier and Andy Way</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1334" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1392">
                        <td>
                            <span class="poster-title">Towards Two-Dimensional Sequence to Sequence Model in Neural Machine Translation.</span>
                            <em>Parnia Bahar, Christopher Brix and Hermann Ney</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1335" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1490">
                        <td>
                            <span class="poster-title">End-to-End Non-Autoregressive Neural Machine Translation with Connectionist Temporal Classification.</span>
                            <em>Jindřich Libovický and Jindřich Helcl</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1336" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1517">
                        <td>
                            <span class="poster-title">Prediction Improves Simultaneous Neural Machine Translation.</span>
                            <em>Ashkan Alinejad, Maryam Siahbani and Anoop Sarkar</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1337" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1571">
                        <td>
                            <span class="poster-title">Training Deeper Neural Machine Translation Models with Transparent Attention.</span>
                            <em>Ankur Bapna, Mia Chen, Orhan Firat, Yuan Cao and Yonghui Wu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1338" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1773">
                        <td>
                            <span class="poster-title">Context and Copying in Neural Machine Translation.</span>
                            <em>Rebecca Knowles and Philipp Koehn</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1339" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1925">
                        <td>
                            <span class="poster-title">Encoding Gated Translation Memory into Neural Machine Translation.</span>
                            <em>Qian Cao and Deyi Xiong</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1340" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1996">
                        <td>
                            <span class="poster-title">Automatic Post-Editing of Machine Translation: A Neural Programmer-Interpreter Approach.</span>
                            <em>Thuy-Trang Vu and Gholamreza Haffari</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1341" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2066">
                        <td>
                            <span class="poster-title">Breaking the Beam Search Curse: A Study of (Re-)Scoring Methods and Stopping Criteria for Neural Machine Translation.</span>
                            <em>Yilin Yang, Liang Huang and Mingbo Ma</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1342" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Multilingual NLP</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="602">
                        <td>
                            <span class="poster-title">Multi-Multi-View Learning: Multilingual and Multi-Representation Entity Typing.</span>
                            <em>Yadollah Yaghoobzadeh and Hinrich Schütze</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1343" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="719">
                        <td>
                            <span class="poster-title">Word Embeddings for Code-Mixed Language Processing.</span>
                            <em>Adithya Pratapa, Monojit Choudhury and Sunayana Sitaram</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1344" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1648">
                        <td>
                            <span class="poster-title">On the Strength of Character Language Models for Multilingual Named Entity Recognition.</span>
                            <em>Xiaodong Yu, Stephen Mayhew, Mark Sammons and Dan Roth</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1345" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1755">
                        <td>
                            <span class="poster-title">Code-switched Language Models Using Dual RNNs and Same-Source Pretraining.</span>
                            <em>Saurabh Garg, Tanmay Parekh and Preethi Jyothi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1346" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2282">
                        <td>
                            <span class="poster-title">Part-of-Speech Tagging for Code-Switched, Transliterated Texts without Explicit Language Identification.</span>
                            <em>Kelsey Ball and Dan Garrette</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1347" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-5">
        <span class="session-title">Mini-Break</span>
        <br/>
        <span class="session-time" title="Saturday, 3 November 2018">14:45 &ndash; 15:00</span>
    </div>
    <div class="session session-expandable session-plenary">
        <div id="expander"></div>
        <a href="#" class="session-title">
            <strong>Keynote II: "Understanding the News that Moves Markets"</strong>
        </a>
        <br/>
        <span class="session-people">
            <a href="https://sites.google.com/site/gideonmann/" target="_blank">Gideon Mann (Bloomberg, L.P.)</a>
        </span>
        <br/>
        <span class="session-time" title="Saturday, 3 November 2018">15:00 &ndash; 16:00</span>
        <br/>
        <span class="session-location btn btn--location">Gold Hall / Copper Hall / Silver Hall / Hall 100</span>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">
                <p>Since the dawn of human civilization, finance and language technology have been connected. However, only recently have advances in statistical language understanding, and an ever-increasing thirst for market advantage, led to the widespread application of natural language technology across the global capital markets. This talk will review the ways in which language technology is enabling market participants to quickly understand and respond to major world events and breaking business news. It will outline the state of the art in applications of NLP to finance and highlight open problems that are being addressed by emerging research.&nbsp;
                    <i class="fa fa-television slides-icon" data="/downloads/keynote-slides/GideonMann.pdf" aria-hidden="true" title="Slides"></i>&nbsp;
                    <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305658007" aria-hidden="true" title="Video"></i>
                </p>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-6">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time" title="Saturday, 3 November 2018">16:00 &ndash; 16:30</span>
    </div>
    <div class="session-box" id="session-box-8">
        <div class="session-header" id="session-header-8">Long Papers &amp; Demos V (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-8a">
            <div id="expander"></div>
            <a href="#" class="session-title">8A: Text Categorization</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-8a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-8a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:IONANDR@GMAIL.COM">Ion Androutsopoulos</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="245">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">Zero-shot User Intent Detection via Capsule Neural Networks.</span>
                            <em>Congying Xia, Chenwei Zhang, Xiaohui Yan, Yi Chang and Philip Yu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1348" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305945714" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="265">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">Hierarchical Neural Networks for Sequential Sentence Classification in Medical Scientific Abstracts.</span>
                            <em>Di Jin and Peter Szolovits</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1349" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305946571" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="291">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">Investigating Capsule Networks with Dynamic Routing for Text Classification.</span>
                            <em>Min Yang, Wei Zhao, Jianbo Ye, Zeyang Lei, Zhou Zhao and Soufei Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1350" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305947408" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="330">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">Topic Memory Networks for Short Text Classification.</span>
                            <em>Jichuan Zeng, Jing Li, Yan Song, Cuiyun Gao, Michael R. Lyu and Irwin King</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1351" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305947994" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="342">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">Few-Shot and Zero-Shot Multi-Label Learning for Structured Label Spaces.</span>
                            <em>Anthony Rios and Ramakanth Kavuluru</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1352" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305948835" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-8b">
            <div id="expander"></div>
            <a href="#" class="session-title">8B: Generation</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-8b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-8b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:i.konstas@hw.ac.uk">Ioannis Konstas</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="300">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">Automatic Poetry Generation with Mutual Reinforcement Learning.</span>
                            <em>Xiaoyuan Yi, Maosong Sun, Ruoyu Li and Wenhao Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1353" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305925622" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="366">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">Variational Autoregressive Decoder for Neural Response Generation.</span>
                            <em>Jiachen Du, Wenjie Li, Yulan He, Ruifeng Xu, Lidong Bing and Xuan Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1354" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305926196" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1746">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">Integrating Transformer and Paraphrase Rules for Sentence Simplification.</span>
                            <em>Sanqiang Zhao, Rui Meng, Daqing He, Andi Saptono and Bambang Parmanto</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1355" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305927122" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2025">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">Learning Neural Templates for Text Generation.</span>
                            <em>Sam Wiseman, Stuart Shieber and Alexander Rush</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1356" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305928599" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2230">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">Multi-Reference Training with Pseudo-References for Neural Translation and Text Generation.</span>
                            <em>Renjie Zheng, Mingbo Ma and Liang Huang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1357" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305929800" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-8c">
            <div id="expander"></div>
            <a href="#" class="session-title">8C: Knowledge Graphs</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-8c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-8c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:ppt@iisc.ac.in">Partha Talukdar</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1000">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">Knowledge Graph Embedding with Hierarchical Relation Structure.</span>
                            <em>Zhao Zhang, Fuzhen Zhuang, Meng Qu, Fen Lin and Qing He</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1358" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306112939" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1331">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">Embedding Multimodal Relational Data for Knowledge Base Completion.</span>
                            <em>Pouya Pezeshkpour, Liyan Chen and Sameer Singh</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1359" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306113486" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1947">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">Multi-Task Identification of Entities, Relations, and Coreference for Scientific Knowledge Graph Construction.</span>
                            <em>Yi Luan, Luheng He, Mari Ostendorf and Hannaneh Hajishirzi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1360" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306113930" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2100">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">Playing 20 Question Game with Policy-Based Reinforcement Learning.</span>
                            <em>Huang Hu, Xianchao Wu, Bingfeng Luo, Chongyang Tao, Can Xu, wei wu and Zhan Chen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1361" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306114592" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2201">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">Multi-Hop Knowledge Graph Reasoning with Reward Shaping.</span>
                            <em>Xi Victoria Lin, Richard Socher and Caiming Xiong</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1362" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306115211" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-8d">
            <div id="expander"></div>
            <a href="#" class="session-title">8D: Morphology / Phonology</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-8d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-8d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:nematzadeh@google.com">Aida Nematzadeh</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="82">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">Neural Transductive Learning and Beyond: Morphological Generation in the Minimal-Resource Setting.</span>
                            <em>Katharina Kann and Hinrich Schütze</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1363" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305676641" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="538">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">Implicational Universals in Stochastic Constraint-Based Phonology.</span>
                            <em>Giorgio Magri</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1364" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305679809" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1533">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">Explaining Character-Aware Neural Networks for Word-Level Prediction: Do They Discover Linguistic Rules?.</span>
                            <em>Fréderic Godin, Kris Demuynck, Joni Dambre, Wesley De Neve and Thomas Demeester</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1365" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305681577" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1860">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">Adapting Word Embeddings to New Languages with Morphological and Phonological Subword Representations.</span>
                            <em>Aditi Chaudhary, Chunting Zhou, Lori Levin, Graham Neubig, David R. Mortensen and Jaime Carbonell</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1366" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305683572" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1420-TACL">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">[TACL] Recurrent Neural Networks in Linguistic Theory: Revisiting Pinker and Prince (1988) and the Past Tense Debate.</span>
                            <em>Christo Kirov, Ryan Cotterell</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="/downloads/tacl-papers/EMNLP-TACL03.pdf" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/305684335" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-8">
            <div id="expander"></div>
            <a href="#" class="session-title">8E: Sentiment, Social Applications, Multimodal Semantics, Discourse (Posters and Demos)</a>
            <br/>
            <span class="session-time" title="Saturday, 3 November 2018">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Discourse</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="470">
                        <td>
                            <span class="poster-title">A Computational Exploration of Exaggeration.</span>
                            <em>Enrica Troiano, Carlo Strapparava, Gözde Özbal and Serra Sinem Tekiroglu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1367" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="665">
                        <td>
                            <span class="poster-title">Building Context-aware Clause Representations for Situation Entity Type Classification.</span>
                            <em>Zeyu Dai and Ruihong Huang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1368" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="704">
                        <td>
                            <span class="poster-title">Hierarchical Dirichlet Gaussian Marked Hawkes Process for Narrative Reconstruction in Continuous Time Domain.</span>
                            <em>Yeon Seonwoo, Alice Oh and Sungjoon Park</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1369" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1489">
                        <td>
                            <span class="poster-title">Investigating the Role of Argumentation in the Rhetorical Analysis of Scientific Publications with Neural Multi-Task Learning Models.</span>
                            <em>Anne Lauscher, Goran Glavaš, Simone Paolo Ponzetto and Kai Eckert</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1370" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1596">
                        <td>
                            <span class="poster-title">Neural Ranking Models for Temporal Dependency Structure Parsing.</span>
                            <em>Yuchen Zhang and Nianwen Xue</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1371" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1554">
                        <td>
                            <span class="poster-title">Causal Explanation Analysis on Social Media.</span>
                            <em>Youngseo Son, Nipun Bayas and H. Andrew Schwartz</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1372" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Recommender Systems</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="113">
                        <td>
                            <span class="poster-title">LRMM: Learning to Recommend with Missing Modalities.</span>
                            <em>Cheng Wang, Mathias Niepert and Hui Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1373" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="481">
                        <td>
                            <span class="poster-title">Content Explorer: Recommending Novel Entities for a Document Writer.</span>
                            <em>Michal Lukasik and Richard Zens</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1374" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="624">
                        <td>
                            <span class="poster-title">A Genre-Aware Attention Model to Improve the Likability Prediction of Books.</span>
                            <em>Suraj Maharjan, Manuel Montes, Fabio A. González and Thamar Solorio</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1375" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1071">
                        <td>
                            <span class="poster-title">Thread Popularity Prediction and Tracking with a Permutation-invariant Model.</span>
                            <em>Hou Pong Chan and Irwin King</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1376" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Sentiment Analysis</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="461">
                        <td>
                            <span class="poster-title">IARM: Inter-Aspect Relation Modeling with Memory Networks in Aspect-Based Sentiment Analysis.</span>
                            <em>Navonil Majumder, Soujanya Poria, Alexander Gelbukh, Md Shad Akhtar, Erik Cambria and Asif Ekbal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1377" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="692">
                        <td>
                            <span class="poster-title">Limbic: Author-Based Sentiment Aspect Modeling Regularized with Word Embeddings and Discourse Relations.</span>
                            <em>Zhe Zhang and Munindar Singh</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1378" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="846">
                        <td>
                            <span class="poster-title">An Interpretable Neural Network with Topical Information for Relevant Emotion Ranking.</span>
                            <em>Yang Yang, Deyu ZHOU and Yulan He</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1379" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1068">
                        <td>
                            <span class="poster-title">Multi-grained Attention Network for Aspect-Level Sentiment Classification.</span>
                            <em>Feifan Fan, Yansong Feng and Dongyan Zhao</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1380" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1651">
                        <td>
                            <span class="poster-title">Attentive Gated Lexicon Reader with Contrastive Contextual Co-Attention for Sentiment Classification.</span>
                            <em>Yi Tay, Anh Tuan Luu, Siu Cheung Hui and Jian Su</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1381" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1824">
                        <td>
                            <span class="poster-title">Contextual Inter-modal Attention for Multi-modal Sentiment Analysis.</span>
                            <em>Deepanway Ghosal, Md Shad Akhtar, Dushyant Chauhan, Soujanya Poria, Asif Ekbal and Pushpak Bhattacharyya</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1382" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1848">
                        <td>
                            <span class="poster-title">Adaptive Semi-supervised Learning for Cross-domain Sentiment Classification.</span>
                            <em>Ruidan He, Wee Sun Lee, Hwee Tou Ng and Daniel Dahlmeier</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1383" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2071">
                        <td>
                            <span class="poster-title">ExtRA: Extracting Prominent Review Aspects from Customer Feedback.</span>
                            <em>Zhiyi Luo, Shanshan Huang, Frank F. Xu, Bill Yuchen Lin, Hanyuan Shi and Kenny Zhu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1384" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Social Applications and Social Media</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="647">
                        <td>
                            <span class="poster-title">Cross-Lingual Cross-Platform Rumor Verification Pivoting on Multimedia Content.</span>
                            <em>Weiming Wen, Songwen Su and Zhou Yu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1385" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="960">
                        <td>
                            <span class="poster-title">Extractive Adversarial Networks: High-Recall Explanations for Identifying Personal Attacks in Social Media Posts.</span>
                            <em>Samuel Carton, Qiaozhu Mei and Paul Resnick</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1386" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1340">
                        <td>
                            <span class="poster-title">Automatic Detection of Vague Words and Sentences in Privacy Policies.</span>
                            <em>Logan Lebanoff and Fei Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1387" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1477">
                        <td>
                            <span class="poster-title">Multi-view Models for Political Ideology Detection of News Articles.</span>
                            <em>Vivek Kulkarni, Junting Ye, Steve Skiena and William Yang Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1388" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1694">
                        <td>
                            <span class="poster-title">Predicting Factuality of Reporting and Bias of News Media Sources.</span>
                            <em>Ramy Baly, Georgi Karadzhov, Dimitar Alexandrov, James Glass and Preslav Nakov</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1389" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1911">
                        <td>
                            <span class="poster-title">Legal Judgment Prediction via Topological Learning.</span>
                            <em>Haoxi Zhong, Guo Zhipeng, Cunchao Tu, Chaojun Xiao, Zhiyuan Liu and Maosong Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1390" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2016">
                        <td>
                            <span class="poster-title">Hierarchical CVAE for Fine-Grained Hate Speech Classification.</span>
                            <em>Jing Qian, Mai ElSherief, Elizabeth Belding and William Yang Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1391" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2107">
                        <td>
                            <span class="poster-title">Residualized Factor Adaptation for Community Social Media Prediction Tasks.</span>
                            <em>Mohammadzaman Zamani, H. Andrew Schwartz, Veronica Lynn, Salvatore Giorgi and Niranjan Balasubramanian</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1392" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2198">
                        <td>
                            <span class="poster-title">Framing and Agenda-setting in Russian News: a Computational Analysis of Intricate Political Strategies.</span>
                            <em>Anjalie Field, Doron Kliger, Shuly Wintner, Jennifer Pan, Dan Jurafsky and Yulia Tsvetkov</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1393" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="479">
                        <td>
                            <span class="poster-title">Identifying the sentiment styles of YouTube's vloggers.</span>
                            <em>Bennett Kleinberg, Maximilian Mozes and Isabelle van der Vegt</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1394" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="862">
                        <td>
                            <span class="poster-title">Native Language Identification with User Generated Content.</span>
                            <em>Gili Goldin, Ella Rabinovich and Shuly Wintner</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1395" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Demos</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="35-demo">
                        <td>
                            <span class="poster-title">Visualization of the Topic Space of Argument Search Results in args.me.</span>
                            <em>Yamen Ajjour, Henning Wachsmuth, Dora Kiesel, Patrick Riehmann, Fan Fan, Giuliano Castiglia, Rosemary Adejoh, Bernd Fröhlich and Benno Stein</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2011" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="44-demo">
                        <td>
                            <span class="poster-title">A Multilingual Information Extraction Pipeline for Investigative Journalism.</span>
                            <em>Gregor Wiedemann, Seid Muhie Yimam and Chris Biemann</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2014" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="75-demo">
                        <td>
                            <span class="poster-title">When science journalism meets artificial intelligence : An interactive demonstration.</span>
                            <em>Raghuram Vadapalli, Bakhtiyar Syed, Nishant Prabhu, Balaji Vasan Srinivasan and Vasudeva Varma</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2028" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-expandable session-plenary" id="session-social">
        <div id="expander"></div>
        <a href="#" class="session-title">Social Event</a>
        <br/>
        <span class="session-time" title="Saturday, 3 November 2018">19:00 &ndash; 22:00</span>
        <br/>
        <span class="session-external-location btn btn--location">Royal Museums of Fine Arts of Belgium</span>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">
                <p>On the evening of Saturday, November 3rd, the EMNLP 2018 social event will take place at the Royal Museums of Fine Arts of Belgium. Four museums, housed in a single building, will welcome the EMNLP delegates with their prestigious collection of 20,000 works of art. The Museums’ collections trace the history of the visual arts — painting, sculpture and drawing — from the 15th to the 21st century.</p>
            </div>
        </div>
    </div>
    <div class="day" id="day-5">Sunday, 4 November 2018</div>
    <div class="session-box" id="session-box-9">
        <div class="session-header" id="session-header-9">Long Papers &amp; Demos VI (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-9a">
            <div id="expander"></div>
            <a href="#" class="session-title">9A: Machine Translation II</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-9a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-9a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:schwenk@fb.com">Holger Schwenk</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="499">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">Beyond Error Propagation in Neural Machine Translation: Characteristics of Language Also Matter.</span>
                            <em>Lijun Wu, Xu Tan, Di He, Fei Tian, Tao Qin, Jianhuang Lai and Tie-Yan Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1396" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306146050" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="979">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">A Study of Reinforcement Learning for Neural Machine Translation.</span>
                            <em>Lijun Wu, Fei Tian, Tao Qin, Jianhuang Lai and Tie-Yan Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1397" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306147010" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1056">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">Meta-Learning for Low-Resource Neural Machine Translation.</span>
                            <em>Jiatao Gu, Yong Wang, Yun Chen, Victor O. K. Li and Kyunghyun Cho</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1398" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306147573" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="455">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">Unsupervised Statistical Machine Translation.</span>
                            <em>Mikel Artetxe, Gorka Labaka and Eneko Agirre</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1399" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306148376" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2187">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">A Visual Attention Grounding Neural Model for Multimodal Machine Translation.</span>
                            <em>Mingyang Zhou, Runxiang Cheng, Yong Jae Lee and Zhou Yu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1400" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306149028" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-9b">
            <div id="expander"></div>
            <a href="#" class="session-title">9B: Sentiment I</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-9b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-9b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:Yulan.He@warwick.ac.uk">Yulan He</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="136">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">Sentiment Classification towards Question-Answering with Hierarchical Matching Network.</span>
                            <em>Chenlin Shen, Changlong Sun, Jingjing Wang, Yangyang Kang, Shoushan Li, Xiaozhong Liu, Luo Si, Min Zhang and Guodong Zhou</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1401" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306126825" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="212">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">Cross-topic Argument Mining from Heterogeneous Sources.</span>
                            <em>Christian Stab, Tristan Miller, Benjamin Schiller, Pranav Rai and Iryna Gurevych</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1402" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306127543" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="335">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">Summarizing Opinions: Aspect Extraction Meets Sentiment Prediction and They Are Both Weakly Supervised.</span>
                            <em>Stefanos Angelidis and Mirella Lapata</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1403" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306128219" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1305">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">CARER: Contextualized Affect Representations for Emotion Recognition.</span>
                            <em>Elvis Saravia, Hsien-Chi Toby Liu, Yen-Hao Huang, Junlin Wu and Yi-Shin Chen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1404" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306129121" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1413-TACL">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">[TACL] Adversarial Deep Averaging Networks for Cross-Lingual Sentiment Classification.</span>
                            <em>Xilun Chen, Yu Sun, Ben Athiwaratkun, Claire Cardie, Kilian Weinberger</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="/downloads/tacl-papers/EMNLP-TACL04.pdf" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306129914" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-9c">
            <div id="expander"></div>
            <a href="#" class="session-title">9C: Machine Learning III</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-9c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-9c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:ravi.sujith@gmail.com">Sujith Ravi</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1358">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">Noise Contrastive Estimation and Negative Sampling for Conditional Models: Consistency and Statistical Efficiency.</span>
                            <em>Zhuang Ma and Michael Collins</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1405" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306156327" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1666">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">CaLcs: Continuously Approximating Longest Common Subsequence for Sequence Level Optimization.</span>
                            <em>Semih Yavuz, Chung-Cheng Chiu, Patrick Nguyen and Yonghui Wu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1406" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306157322" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2051">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">Pathologies of Neural Models Make Interpretations Difficult.</span>
                            <em>Shi Feng, Eric Wallace, Alvin Grissom II, Mohit Iyyer, Pedro Rodriguez and Jordan Boyd-Graber</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1407" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306158589" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="758">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">Phrase-level Self-Attention Networks for Universal Sentence Encoding.</span>
                            <em>Wei Wu, Houfeng Wang, Tianyu Liu and Shuming Ma</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1408" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306159624" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1322">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">BanditSum: Extractive Summarization as a Contextual Bandit.</span>
                            <em>Yue Dong, Yikang Shen, Eric Crawford, Herke van Hoof and Jackie Chi Kit Cheung</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1409" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306160623" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-9d">
            <div id="expander"></div>
            <a href="#" class="session-title">9D: Semantics VI</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-9d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-9d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:gabriel.satanovsky@gmail.com">Gabriel Stanovsky</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="652">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">A Word-Complexity Lexicon and A Neural Readability Ranking Model for Lexical Simplification.</span>
                            <em>Mounica Maddela and Wei Xu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1410" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306116474" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1411">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">Learning Latent Semantic Annotations for Grounding Natural Language to Structured Data.</span>
                            <em>Guanghui Qin, Jin-Ge Yao, Xuening Wang, Jinpeng Wang and Chin-Yew Lin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1411" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306117499" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2060">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">Syntactic Scaffolds for Semantic Structures.</span>
                            <em>Swabha Swayamdipta, Sam Thomson, Kenton Lee, Luke Zettlemoyer, Chris Dyer and Noah A. Smith</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1412" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306118515" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2103">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">Hierarchical Quantized Representations for Script Generation.</span>
                            <em>Noah Weber, Leena Shekhar, Niranjan Balasubramanian and Nate Chambers</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1413" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306119229" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2250">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">Semantic Role Labeling for Learner Chinese: the Importance of Syntactic Parsing and L2-L1 Parallel Data.</span>
                            <em>Zi Lin, Yuguang Duan, Yuanyuan Zhao, Weiwei Sun and Xiaojun Wan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1414" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306119942" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-9">
            <div id="expander"></div>
            <a href="#" class="session-title">9E: Generation, Dialogue, Summarization; Vision &amp; Language II (Posters and Demos)</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">09:00 &ndash; 10:30</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Dialogue</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="305">
                        <td>
                            <span class="poster-title">A Teacher-Student Framework for Maintainable Dialog Manager.</span>
                            <em>Weikang Wang, Jiajun Zhang, Han Zhang, Mei-Yuh Hwang, Chengqing Zong and Zhifei Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1415" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1511">
                        <td>
                            <span class="poster-title">Discriminative Deep Dyna-Q: Robust Planning for Dialogue Policy Learning.</span>
                            <em>Shang-Yu Su, Xiujun Li, Jianfeng Gao, Jingjing Liu and Yun-Nung Chen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1416" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1572">
                        <td>
                            <span class="poster-title">A Self-Attentive Model with Gate Mechanism for Spoken Language Understanding.</span>
                            <em>Changliang Li, Liang Li and Ji Qi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1417" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1779">
                        <td>
                            <span class="poster-title">Learning End-to-End Goal-Oriented Dialog with Multiple Answers.</span>
                            <em>Janarthanan Rajendran, Jatin Ganhotra, Satinder Singh and Lazaros Polymenakos</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1418" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2138">
                        <td>
                            <span class="poster-title">AirDialogue: An Environment for Goal-Oriented Dialogue Research.</span>
                            <em>Wei Wei, Quoc Le, Andrew Dai and Jia Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1419" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1424-TACL">
                        <td>
                            <span class="poster-title">[TACL] Polite Dialogue Generation Without Parallel Data.</span>
                            <em>Tong Niu and Mohit Bansal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="/downloads/tacl-papers/EMNLP-TACL05.pdf" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Generation</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="377">
                        <td>
                            <span class="poster-title">QuaSE: Sequence Editing under Quantifiable Guidance.</span>
                            <em>Yi Liao, Lidong Bing, Piji Li, Shuming Shi, Wai Lam and Tong Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1420" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="413">
                        <td>
                            <span class="poster-title">Paraphrase Generation with Deep Reinforcement Learning.</span>
                            <em>Zichao Li, Xin Jiang, Lifeng Shang and Hang Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1421" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="447">
                        <td>
                            <span class="poster-title">Operation-guided Neural Networks for High Fidelity Data-To-Text Generation.</span>
                            <em>Feng Nie, Jinpeng Wang, Jin-Ge Yao, Rong Pan and Chin-Yew Lin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1422" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="462">
                        <td>
                            <span class="poster-title">Generating Classical Chinese Poems via Conditional Variational Autoencoder and Adversarial Training.</span>
                            <em>Juntao Li, Yan Song, Haisong Zhang, Dongmin Chen, Shuming Shi, Dongyan Zhao and Rui Yan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1423" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="529">
                        <td>
                            <span class="poster-title">Paragraph-level Neural Question Generation with Maxout Pointer and Gated Self-attention Networks.</span>
                            <em>Yao Zhao, Xiaochuan Ni, Yuanyuan Ding and Qifa Ke</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1424" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1262">
                        <td>
                            <span class="poster-title">Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task.</span>
                            <em>Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingning Yao, Shanelle Roman, Zilin Zhang and Dragomir Radev</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1425" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="65">
                        <td>
                            <span class="poster-title">Unsupervised Natural Language Generation with Denoising Autoencoders.</span>
                            <em>Markus Freitag and Scott Roy</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1426" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1714">
                        <td>
                            <span class="poster-title">Answer-focused and Position-aware Neural Question Generation.</span>
                            <em>Xingwu Sun, Jing Liu, Yajuan Lyu, Wei He, Yanjun Ma and Shi Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1427" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1818">
                        <td>
                            <span class="poster-title">Diversity-Promoting GAN: A Cross-Entropy Based Generative Adversarial Network for Diversified Text Generation.</span>
                            <em>Jingjing Xu, Xuancheng Ren, Junyang Lin and Xu Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1428" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2039">
                        <td>
                            <span class="poster-title">Towards a Better Metric for Evaluating Question Generation Systems.</span>
                            <em>Preksha Nema and Mitesh M. Khapra</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1429" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="866">
                        <td>
                            <span class="poster-title">Stylistic Chinese Poetry Generation via Unsupervised Style Disentanglement.</span>
                            <em>Cheng Yang, Maosong Sun, Xiaoyuan Yi and Wenhao Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1430" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1127">
                        <td>
                            <span class="poster-title">Generating More Interesting Responses in Neural Conversation Models with Distributional Constraints.</span>
                            <em>Ashutosh Baheti, Alan Ritter, Jiwei Li and Bill Dolan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1431" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1241">
                        <td>
                            <span class="poster-title">Better Conversations by Modeling, Filtering, and Optimizing for Coherence and Diversity.</span>
                            <em>Xinnuo Xu, Ondřej Dušek, Ioannis Konstas and Verena Rieser</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1432" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Vision and Language</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="227">
                        <td>
                            <span class="poster-title">Incorporating Background Knowledge into Video Description Generation.</span>
                            <em>Spencer Whitehead, Heng Ji, Mohit Bansal, Shih-Fu Chang and Clare Voss</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1433" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="229">
                        <td>
                            <span class="poster-title">Multimodal Differential Network for Visual Question Generation.</span>
                            <em>Badri Narayana Patro, Sandeep Kumar, Vinod Kumar Kurmi and Vinay Namboodiri</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1434" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="232">
                        <td>
                            <span class="poster-title">Entity-aware Image Caption Generation.</span>
                            <em>Di Lu, Spencer Whitehead, Lifu Huang, Heng Ji and Shih-Fu Chang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1435" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1900">
                        <td>
                            <span class="poster-title">Learning to Describe Differences Between Pairs of Similar Images.</span>
                            <em>Harsh Jhamtani and Taylor Berg-Kirkpatrick</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1436" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2074">
                        <td>
                            <span class="poster-title">Object Hallucination in Image Captioning.</span>
                            <em>Anna Rohrbach, Lisa Anne Hendricks, Kaylee Burns, Trevor Darrell and Kate Saenko</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1437" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="206">
                        <td>
                            <span class="poster-title">Abstractive Text-Image Summarization Using Multi-Modal Attentional Hierarchical RNN.</span>
                            <em>Jingqiang Chen and Hai Zhuge</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1438" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Summarization</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="207">
                        <td>
                            <span class="poster-title">Keyphrase Generation with Correlation Constraints.</span>
                            <em>Jun Chen, Xiaoming Zhang, Yu Wu, Zhao Yan and Zhoujun Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1439" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="585">
                        <td>
                            <span class="poster-title">Closed-Book Training to Improve Summarization Encoder Memory.</span>
                            <em>Yichen Jiang and Mohit Bansal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1440" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="727">
                        <td>
                            <span class="poster-title">Improving Neural Abstractive Document Summarization with Structural Regularization.</span>
                            <em>Wei Li, Xinyan Xiao, Yajuan Lyu and Yuanzhuo Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1441" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="950">
                        <td>
                            <span class="poster-title">Iterative Document Representation Learning Towards Summarization with Polishing.</span>
                            <em>Xiuying Chen, Shen Gao, Chongyang Tao, Yan Song, Dongyan Zhao and Rui Yan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1442" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1181">
                        <td>
                            <span class="poster-title">Bottom-Up Abstractive Summarization.</span>
                            <em>Sebastian Gehrmann, Yuntian Deng and Alexander Rush</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1443" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1192">
                        <td>
                            <span class="poster-title">Controlling Length in Abstractive Summarization Using a Convolutional Neural Network.</span>
                            <em>Yizhu Liu, Zhiyi Luo and Kenny Zhu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1444" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1293">
                        <td>
                            <span class="poster-title">APRIL: Interactively Learning to Summarise by Combining Active Preference Learning and Reinforcement Learning.</span>
                            <em>Yang Gao, Christian M. Meyer and Iryna Gurevych</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1445" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1324">
                        <td>
                            <span class="poster-title">Adapting the Neural Encoder-Decoder Framework from Single to Multi-Document Summarization.</span>
                            <em>Logan Lebanoff, Kaiqiang Song and Fei Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1446" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1362">
                        <td>
                            <span class="poster-title">Semi-Supervised Learning for Neural Keyphrase Generation.</span>
                            <em>Hai Ye and Lu Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1447" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1482">
                        <td>
                            <span class="poster-title">MSMO: Multimodal Summarization with Multimodal Output.</span>
                            <em>Junnan Zhu, Haoran Li, Tianshang Liu, Yu Zhou, Jiajun Zhang and Chengqing Zong</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1448" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1539">
                        <td>
                            <span class="poster-title">Frustratingly Easy Model Ensemble for Abstractive Summarization.</span>
                            <em>Hayato Kobayashi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1449" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1575">
                        <td>
                            <span class="poster-title">Automatic Pyramid Evaluation Exploiting EDU-based Extractive Reference Summaries.</span>
                            <em>Tsutomu Hirao, Hidetaka Kamigaito and Masaaki Nagata</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1450" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1975">
                        <td>
                            <span class="poster-title">Learning to Encode Text as Human-Readable Summaries using Generative Adversarial Networks.</span>
                            <em>Yaushian Wang and Hung-yi Lee</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1451" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Demos</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="56-demo">
                        <td>
                            <span class="poster-title">Visualizing Group Dynamics based on Multiparty Meeting Understanding.</span>
                            <em>Ni Zhang, Tongtao Zhang, Indrani Bhattacharya, Heng Ji and Rich Radke</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2017" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="70-demo">
                        <td>
                            <span class="poster-title">PizzaPal: Conversational Pizza Ordering using a High-Density Conversational AI Platform.</span>
                            <em>Antoine Raux, Yi Ma, Paul Yang and Felicia Wong</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2026" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="71-demo">
                        <td>
                            <span class="poster-title">Developing Production-Level Conversational Interfaces with Shallow Semantic Parsing.</span>
                            <em>Arushi Raghuvanshi, Lucien Carroll and Karthik Raghunathan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2027" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="7-demo">
                        <td>
                            <span class="poster-title">SyntaViz: Visualizing Voice Queries through a Syntax-Driven Hierarchical Ontology.</span>
                            <em>Md Iftekhar Tanveer and Ferhan Ture</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2001" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="69-demo">
                        <td>
                            <span class="poster-title">LIA: A Natural Language Programmable Personal Assistant.</span>
                            <em>Igor Labutov, Shashank Srivastava and Tom Mitchell</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2025" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="10-demo">
                        <td>
                            <span class="poster-title">Data2Text Studio: Automated Text Generation from Structured Data.</span>
                            <em>Longxu Dou, Guanghui Qin, Jinpeng Wang, Jin-Ge Yao and Chin-Yew Lin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2003" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="32-demo">
                        <td>
                            <span class="poster-title">Demonstrating Par4Sem - A Semantic Writing Aid with Adaptive Paraphrasing.</span>
                            <em>Seid Muhie Yimam and Chris Biemann</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2009" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-7">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time" title="Sunday, 4 November 2018">10:30 &ndash; 11:00</span>
    </div>
    <div class="session-box" id="session-box-10">
        <div class="session-header" id="session-header-10">Long Papers &amp; Demos VII (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-10a">
            <div id="expander"></div>
            <a href="#" class="session-title">10A: Question Answering III</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-10a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-10a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:jbg@umiacs.umd.edu">Jordan Boyd-Graber</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="587">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">Joint Multitask Learning for Community Question Answering Using Task-Specific Embeddings.</span>
                            <em>Shafiq Joty, Lluís Màrquez and Preslav Nakov</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1452" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306149753" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1017">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">What Makes Reading Comprehension Questions Easier?.</span>
                            <em>Saku Sugawara, Kentaro Inui, Satoshi Sekine and Akiko Aizawa</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1453" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306150555" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1989">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">Commonsense for Generative Multi-Hop Question Answering Tasks.</span>
                            <em>Lisa Bauer, Yicheng Wang and Mohit Bansal</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1454" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306151626" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2043">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Open Domain Question Answering Using Early Fusion of Knowledge Bases and Text.</span>
                            <em>Haitian Sun, Bhuwan Dhingra, Manzil Zaheer, Kathryn Mazaitis, Ruslan Salakhutdinov and William Cohen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1455" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306152381" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2134">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">A Nil-Aware Answer Extraction Framework for Question Answering.</span>
                            <em>Souvik Kundu and Hwee Tou Ng</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1456" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306152896" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-10b">
            <div id="expander"></div>
            <a href="#" class="session-title">10B: Machine Translation III</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-10b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-10b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:jorg.tiedemann@helsinki.fi">Joerg Tiedemann</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1021">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">Exploiting Deep Representations for Neural Machine Translation.</span>
                            <em>Zi-Yi Dou, Zhaopeng Tu, Xing Wang, Shuming Shi and Tong Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1457" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306130778" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1129">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">Why Self-Attention? A Targeted Evaluation of Neural Machine Translation Architectures.</span>
                            <em>Gongbo Tang, Mathias Müller, Annette Rios and Rico Sennrich</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1458" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306131741" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1507">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">Simplifying Neural Machine Translation with Addition-Subtraction Twin-Gated Recurrent Networks.</span>
                            <em>Biao Zhang, Deyi Xiong, jinsong su, Qian Lin and Huiji Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1459" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306132998" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2064">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Speeding Up Neural Machine Translation Decoding by Cube Pruning.</span>
                            <em>Wen Zhang, Liang Huang, Yang Feng, Lei Shen and Qun Liu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1460" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306134160" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2304">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Revisiting Character-Based Neural Machine Translation with Capacity and Compression.</span>
                            <em>Colin Cherry, George Foster, Ankur Bapna, Orhan Firat and Wolfgang Macherey</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1461" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306134793" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-10c">
            <div id="expander"></div>
            <a href="#" class="session-title">10C: Discourse</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-10c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-10c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:mlap@inf.ed.ac.uk">Mirella Lapata</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="907">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">A Skeleton-Based Model for Promoting Coherence Among Sentences in Narrative Story Generation.</span>
                            <em>Jingjing Xu, Xuancheng Ren, Yi Zhang, Qi Zeng, Xiaoyan Cai and Xu Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1462" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306161720" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="968">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">NEXUS Network: Connecting the Preceding and the Following in Dialogue Generation.</span>
                            <em>Xiaoyu Shen, Hui Su, Wenjie Li and Dietrich Klakow</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1463" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306163081" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1138">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">A Neural Local Coherence Model for Text Quality Assessment.</span>
                            <em>Mohsen Mesgar and Michael Strube</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1464" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306164201" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1268">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Deep Attentive Sentence Ordering Network.</span>
                            <em>Baiyun Cui, Yingming Li, Ming Chen and Zhongfei Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1465" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306165142" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1276">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Getting to "Hearer-old": Charting Referring Expressions Across Time.</span>
                            <em>Ieva Staliūnaitė, Hannah Rohde, Bonnie Webber and Annie Louis</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1466" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306166016" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-10d">
            <div id="expander"></div>
            <a href="#" class="session-title">10D: Evolution / Sociolinguistics</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-10d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-10d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:jurgens@umich.edu">David Jurgens</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="63">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">Making "fetch" happen: The influence of social and linguistic context on nonstandard word growth and decline.</span>
                            <em>Ian Stewart and Jacob Eisenstein</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1467" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306120421" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="357">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">Analyzing Correlated Evolution of Multiple Features Using Latent Representations.</span>
                            <em>Yugo Murawaki</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1468" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306121200" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="486">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">Capturing Regional Variation with Distributed Place Representations and Geographic Retrofitting.</span>
                            <em>Dirk Hovy and Christoph Purschke</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1469" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306121832" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1702">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">Characterizing Interactions and Relationships between People.</span>
                            <em>Farzana Rashid and Eduardo Blanco</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1470" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306122681" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2160">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">Why Swear? Analyzing and Inferring the Intentions of Vulgar Expressions.</span>
                            <em>Eric Holgate, Isabel Cachola, Daniel Preoţiuc-Pietro and Junyi Jessy Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1471" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306123618" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-10">
            <div id="expander"></div>
            <a href="#" class="session-title">10E: Machine Learning (Posters and Demos)</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Architectures and Models</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="500">
                        <td>
                            <span class="poster-title">A Probabilistic Annotation Model for Crowdsourcing Coreference.</span>
                            <em>Silviu Paun, Jon Chamberlain, Udo Kruschwitz, Juntao Yu and Massimo Poesio</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1218" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="256">
                        <td>
                            <span class="poster-title">Is it Time to Swish? Comparing Deep Learning Activation Functions Across NLP tasks.</span>
                            <em>Steffen Eger, Paul Youssef and Iryna Gurevych</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1472" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="648">
                        <td>
                            <span class="poster-title">Hard Non-Monotonic Attention for Character-Level Transduction.</span>
                            <em>Shijie Wu, Pamela Shapiro and Ryan Cotterell</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1473" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="689">
                        <td>
                            <span class="poster-title">Speed Reading: Learning to Read ForBackward via Shuttle.</span>
                            <em>Tsu-Jui Fu and Wei-Yun Ma</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1474" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1026">
                        <td>
                            <span class="poster-title">Modeling Localness for Self-Attention Networks.</span>
                            <em>Baosong Yang, Zhaopeng Tu, Derek F. Wong, Fandong Meng, Lidia S. Chao and Tong Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1475" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1050">
                        <td>
                            <span class="poster-title">Chargrid: Towards Understanding 2D Documents.</span>
                            <em>Anoop R Katti, Christian Reisswig, Cordula Guder, Sebastian Brarda, Steffen Bickel, Johannes Höhne and Jean Baptiste Faddoul</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1476" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1562">
                        <td>
                            <span class="poster-title">Simple Recurrent Units for Highly Parallelizable Recurrence.</span>
                            <em>Tao Lei, Yu Zhang, Sida I. Wang, Hui Dai and Yoav Artzi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1477" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1598">
                        <td>
                            <span class="poster-title">NPRF: A Neural Pseudo Relevance Feedback Framework for Ad-hoc Information Retrieval.</span>
                            <em>Canjia Li, Yingfei Sun, Ben He, Le Wang, Kai Hui, Andrew Yates, Le Sun and Jungang Xu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1478" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1691">
                        <td>
                            <span class="poster-title">Co-Stack Residual Affinity Networks with Multi-level Attention Refinement for Matching Text Sequences.</span>
                            <em>Yi Tay, Anh Tuan Luu and Siu Cheung Hui</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1479" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1720">
                        <td>
                            <span class="poster-title">Spherical Latent Spaces for Stable Variational Autoencoders.</span>
                            <em>Jiacheng Xu and Greg Durrett</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1480" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1869">
                        <td>
                            <span class="poster-title">Learning Universal Sentence Representations with Mean-Max Attention Autoencoder.</span>
                            <em>Minghua Zhang, Yunfang Wu, Weikang Li and Wei Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1481" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1891">
                        <td>
                            <span class="poster-title">Word Mover's Embedding: From Word2Vec to Document Embedding.</span>
                            <em>Lingfei Wu, Ian En-Hsu Yen, Kun Xu, Fangli Xu, Avinash Balakrishnan, Pin-Yu Chen, Pradeep Ravikumar and Michael J. Witbrock</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1482" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1221">
                        <td>
                            <span class="poster-title">Learning Disentangled Representations of Texts with Application to Biomedical Abstracts.</span>
                            <em>Sarthak Jain, Edward Banner, Jan-Willem van de Meent, Iain J Marshall and Byron C. Wallace</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1497" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1781">
                        <td>
                            <span class="poster-title">Multi-Source Domain Adaptation with Mixture of Experts.</span>
                            <em>Jiang Guo, Darsh Shah and Regina Barzilay</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1498" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1898">
                        <td>
                            <span class="poster-title">HyTE: Hyperplane-based Temporally aware Knowledge Graph Embedding.</span>
                            <em>Shib Sankar Dasgupta, Swayambhu Nath Ray and Partha Talukdar</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1225" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Text Classification and Topic Modeling</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="707">
                        <td>
                            <span class="poster-title">Multilingual Clustering of Streaming News.</span>
                            <em>Sebastião Miranda, Arturs Znotins, Shay B. Cohen and Guntis Barzdins</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1483" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="744">
                        <td>
                            <span class="poster-title">Multi-Task Label Embedding for Text Classification.</span>
                            <em>Honglun Zhang, Liqiang Xiao, Wenqing Chen, Yongkun Wang and Yaohui Jin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1484" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1235">
                        <td>
                            <span class="poster-title">Semantic-Unit-Based Dilated Convolution for Multi-Label Text Classification.</span>
                            <em>Junyang Lin, Qi Su, Pengcheng Yang, Shuming Ma and Xu Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1485" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1512">
                        <td>
                            <span class="poster-title">MCapsNet: Capsule Network for Text with Multi-Task Learning.</span>
                            <em>Liqiang Xiao, Honglun Zhang, Wenqing Chen, Yongkun Wang and Yaohui Jin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1486" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1738">
                        <td>
                            <span class="poster-title">Uncertainty-aware generative models for inferring document class prevalence.</span>
                            <em>Katherine Keith and Brendan O'Connor</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1487" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2087">
                        <td>
                            <span class="poster-title">Challenges of Using Text Classifiers for Causal Inference.</span>
                            <em>Zach Wood-Doughty, Ilya Shpitser and Mark Dredze</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1488" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="912">
                        <td>
                            <span class="poster-title">Siamese Network-Based Supervised Topic Modeling.</span>
                            <em>Minghui Huang, Yanghui Rao, Yuwei Liu, Haoran Xie and Fu Lee Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1494" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1877">
                        <td>
                            <span class="poster-title">GraphBTM: Graph Enhanced Autoencoded Variational Inference for Biterm Topic Model.</span>
                            <em>Qile Zhu, Zheng Feng and Xiaolin Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1495" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2098">
                        <td>
                            <span class="poster-title">Modeling Online Discourse with Coupled Distributed Topics.</span>
                            <em>Akshay Srivatsan, Zachary Wojtowicz and Taylor Berg-Kirkpatrick</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1496" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Language Modeling</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="709">
                        <td>
                            <span class="poster-title">Direct Output Connection for a High-Rank Language Model.</span>
                            <em>Sho Takase, Jun Suzuki and Masaaki Nagata</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1489" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1465">
                        <td>
                            <span class="poster-title">Disfluency Detection using Auto-Correlational Neural Networks.</span>
                            <em>Paria Jamshid Lou, Peter Anderson and Mark Johnson</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1490" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1479">
                        <td>
                            <span class="poster-title">Pyramidal Recurrent Unit for Language Modeling.</span>
                            <em>Sachin Mehta, Rik Koncel-Kedziorski, Mohammad Rastegari and Hannaneh Hajishirzi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1491" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1793">
                        <td>
                            <span class="poster-title">On Tree-Based Neural Sentence Modeling.</span>
                            <em>Haoyue Shi, Hao Zhou, Jiaze Chen and Lei Li</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1492" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1962">
                        <td>
                            <span class="poster-title">Language Modeling with Sparse Product of Sememe Experts.</span>
                            <em>Yihong Gu, Jun Yan, Hao Zhu, Zhiyuan Liu, Ruobing Xie, Maosong Sun, Fen Lin and Leyu Lin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1493" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1379-TACL">
                        <td>
                            <span class="poster-title">[TACL] Language Modeling for Morphologically Rich Languages: Character-Aware Modeling for Word-Level Prediction.</span>
                            <em>Daniela Gerz, Ivan Vulić, Edoardo Maria Ponti, Jason Naradowsky, Roi Reichart, Anna Korhonen</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1396-TACL">
                        <td>
                            <span class="poster-title">[TACL] Low-Rank RNN Adaptation for Context-Aware Language Modeling.</span>
                            <em>Aaron Jaech and Mari Ostendorf</em>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Demos</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="49-demo">
                        <td>
                            <span class="poster-title">Sisyphus, a Workflow Manager Designed for Machine Translation and Automatic Speech Recognition.</span>
                            <em>Jan-Thorsten Peter, Eugen Beck and Hermann Ney</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2015" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="59-demo">
                        <td>
                            <span class="poster-title">APLenty: annotation tool for creating high-quality datasets using active and proactive learning.</span>
                            <em>Minh-Quoc Nghiem and Sophia Ananiadou</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2019" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="53-demo">
                        <td>
                            <span class="poster-title">KT-Speech-Crawler: Automatic Dataset Construction for Speech Recognition from YouTube Videos.</span>
                            <em>Egor Lakomkin, Sven Magg, Cornelius Weber and Stefan Wermter</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2016" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="15-demo">
                        <td>
                            <span class="poster-title">Term Set Expansion based NLP Architect by Intel AI Lab.</span>
                            <em>Jonathan Mamou, Oren Pereg, Moshe Wasserblat, Alon Eirew, Yael Green, Shira Guskin, Peter Izsak and Daniel Korat</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-2004" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-5">
        <span class="session-title">Lunch</span>
        <br/>
        <span class="session-time" title="Sunday, 4 November 2018">12:30 &ndash; 13:00</span>
    </div>
    <div class="session session-expandable session-plenary" id="session-business">
        <div id="expander"></div>
        <a href="#" class="session-title">SIGDAT Business Meeting</a>
        <br/>
        <span class="session-time" title="Sunday, 4 November 2018">13:00 &ndash; 13:45</span>
        <br/>
        <span class="session-location btn btn--location">Copper Hall</span>
        <br/>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">All attendees are encouraged to participate in the business meeting.</div>
        </div>
    </div>
    <div class="session-box" id="session-box-11">
        <div class="session-header" id="session-header-11">Short Papers IV (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-11a">
            <div id="expander"></div>
            <a href="#" class="session-title">11A: Analyzing Models</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-11a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-11a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:lsz@cs.washington.edu">Luke Zettlemoyer</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="657">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">A Neural Model of Adaptation in Reading.</span>
                            <em>Marten van Schijndel and Tal Linzen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1499" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306153668" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="103">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Understanding Deep Learning Performance through an Examination of Test Set Difficulty: A Psychometric Case Study.</span>
                            <em>John Lalor, Hao Wu, Tsendsuren Munkhdalai and Hong Yu</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1500" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306154181" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1369">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">Lexicosyntactic Inference in Neural Models.</span>
                            <em>Aaron Steven White, Rachel Rudinger, Kyle Rawlins and Benjamin Van Durme</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1501" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306154470" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="695">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Dual Fixed-Size Ordinally Forgetting Encoding (FOFE) for Competitive Neural Language Models.</span>
                            <em>Sedtawut Watcharawittayakul, Mingbin Xu and Hui Jiang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1502" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306154936" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="204">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">The Importance of Being Recurrent for Modeling Hierarchical Structure.</span>
                            <em>Ke Tran, Arianna Bisazza and Christof Monz</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1503" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306155520" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-11b">
            <div id="expander"></div>
            <a href="#" class="session-title">11B: Sentiment II</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Copper Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-11b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-11b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:thamar.solorio@gmail.com">Thamar Solorio</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1664">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">Joint Learning for Targeted Sentiment Analysis.</span>
                            <em>Dehong Ma, Sujian Li and Houfeng Wang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1504" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306135717" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2092">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Revisiting the Importance of Encoding Logic Rules in Sentiment Classification.</span>
                            <em>Kalpesh Krishna, Preethi Jyothi and Mohit Iyyer</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1505" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306136412" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1622">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">A Co-Attention Neural Network Model for Emotion Cause Analysis with Emotional Context Awareness.</span>
                            <em>Xiangju Li, Kaisong Song, Shi Feng, Daling Wang and Yifei Zhang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1506" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306136988" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1217">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Modeling Empathy and Distress in Reaction to News Stories.</span>
                            <em>Sven Buechel, Anneke Buffone, Barry Slaff, Lyle Ungar and Joao Sedoc</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1507" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306137544" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1497">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">Interpretable Emoji Prediction via Label-Wise Attention LSTMs.</span>
                            <em>Francesco Barbieri, Luis Espinosa Anke, Jose Camacho-Collados, Steven Schockaert and Horacio Saggion</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1508" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306138266" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-11c">
            <div id="expander"></div>
            <a href="#" class="session-title">11C: Machine Translation IV</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Silver Hall / Panoramic Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-11c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-11c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:tarow@google.com">Taro Watanabe</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="958">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">A Tree-based Decoder for Neural Machine Translation.</span>
                            <em>Xinyi Wang, Hieu Pham, Pengcheng Yin and Graham Neubig</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1509" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306166768" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1176">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">Greedy Search with Probabilistic N-gram Matching for Neural Machine Translation.</span>
                            <em>Chenze Shao, Xilin Chen and Yang Feng</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1510" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306167593" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="464">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">Exploring Recombination for Efficient Decoding of Neural Machine Translation.</span>
                            <em>Zhisong Zhang, Rui Wang, Masao Utiyama, Eiichiro Sumita and Hai Zhao</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1511" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306168250" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1267">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Has Machine Translation Achieved Human Parity? A Case for Document-level Evaluation.</span>
                            <em>Samuel Läubli, Rico Sennrich and Martin Volk</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1512" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306169001" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1150">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">Automatic Reference-Based Evaluation of Pronoun Translation Misses the Point.</span>
                            <em>Liane Guillou and Christian Hardmeier</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1513" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306169819" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-11d">
            <div id="expander"></div>
            <a href="#" class="session-title">11D: QA / Knowledge Graphs</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Hall 100 / Hall 400</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-11d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-11d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair:
                            <a href="mailto:beroth@cis.uni-muenchen.de">Benjamin Roth</a>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2190">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">FewRel: A Large-Scale Supervised Few-Shot Relation Classification Dataset with State-of-the-Art Evaluation.</span>
                            <em>Xu Han, Hao Zhu, Pengfei Yu, Ziyun Wang, Yuan Yao, Zhiyuan Liu and Maosong Sun</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1514" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306124333" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1270">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">A strong baseline for question relevancy ranking.</span>
                            <em>Ana Gonzalez, Isabelle Augenstein and Anders Søgaard</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1515" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306167593" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="946">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">Learning Sequence Encoders for Temporal Knowledge Graph Completion.</span>
                            <em>Alberto Garcia-Duran, Sebastijan Dumančić and Mathias Niepert</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1516" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306125393" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="152">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">Similar but not the Same: Word Sense Disambiguation Improves Event Detection via Neural Representation Matching.</span>
                            <em>Weiyi Lu and Thien Huu Nguyen</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1517" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306125936" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="1440">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">Learning Word Representations with Cross-Sentence Dependency for End-to-End Co-reference Resolution.</span>
                            <em>Hongyin Luo and Jim Glass</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1518" aria-hidden="true" title="PDF"></i>&nbsp;
                            <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306126460" aria-hidden="true" title="Video"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-11">
            <div id="expander"></div>
            <a href="#" class="session-title">11E: Short Posters IV</a>
            <br/>
            <span class="session-time" title="Sunday, 4 November 2018">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--location">Grand Hall</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr>
                        <td>
                            <span class="poster-type">Morphology</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="589">
                        <td>
                            <span class="poster-title">State-of-the-art Chinese Word Segmentation with Bi-LSTMs.</span>
                            <em>Ji Ma, Kuzman Ganchev and David Weiss</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1529" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="901">
                        <td>
                            <span class="poster-title">Sanskrit Sandhi Splitting using seq2(seq)2.</span>
                            <em>Rahul Aralikatte, Neelamadhav Gantayat, Naveen Panwar, Anush Sankaran and Senthil Mani</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1530" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1120">
                        <td>
                            <span class="poster-title">Unsupervised Neural Word Segmentation for Chinese via Segmental Language Modeling.</span>
                            <em>Zhiqing Sun and Zhi-Hong Deng</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1531" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1543">
                        <td>
                            <span class="poster-title">LemmaTag: Jointly Tagging and Lemmatizing for Morphologically Rich Languages with BRNNs.</span>
                            <em>Daniel Kondratyuk, Tomáš Gavenčiak, Milan Straka and Jan Hajič</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1532" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2298">
                        <td>
                            <span class="poster-title">Recovering Missing Characters in Old Hawaiian Writing.</span>
                            <em>Brendan Shillingford and Oiwi Parker Jones</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1533" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Syntax</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="875">
                        <td>
                            <span class="poster-title">Wronging a Right: Generating Better Errors to Improve Grammatical Error Detection.</span>
                            <em>Sudhanshu Kasewa, Pontus Stenetorp and Sebastian Riedel</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/ [D18-1541]" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1307">
                        <td>
                            <span class="poster-title">Modeling Input Uncertainty in Neural Network Dependency Parsing.</span>
                            <em>Rob van der Goot and Gertjan van Noord</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1542" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1373">
                        <td>
                            <span class="poster-title">Parameter sharing between dependency parsers for related languages.</span>
                            <em>Miryam de Lhoneux, Johannes Bjerva, Isabelle Augenstein and Anders Søgaard</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1543" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2165">
                        <td>
                            <span class="poster-title">Grammar Induction with Neural Language Models: An Unusual Replication.</span>
                            <em>Phu Mon Htut, Kyunghyun Cho and Samuel Bowman</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1544" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2183">
                        <td>
                            <span class="poster-title">Data Augmentation via Dependency Tree Morphing for Low-Resource Languages.</span>
                            <em>Gozde Gul Sahin and Mark Steedman</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1545" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Lexical Semantics</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="821">
                        <td>
                            <span class="poster-title">Word Relation Autoencoder for Unseen Hypernym Extraction Using Word Embeddings.</span>
                            <em>Hong-You Chen, Cheng-Syuan Lee, Keng-Te Liao and Shou-de Lin</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1519" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1059">
                        <td>
                            <span class="poster-title">Refining Pretrained Word Embeddings Using Layer-wise Relevance Propagation.</span>
                            <em>Akira Utsumi</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1520" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1098">
                        <td>
                            <span class="poster-title">Learning Gender-Neutral Word Embeddings.</span>
                            <em>Jieyu Zhao, Yichao Zhou, Zeyu Li, Wei Wang and Kai-Wei Chang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1521" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1190">
                        <td>
                            <span class="poster-title">Learning Concept Abstractness Using Weak Supervision.</span>
                            <em>Ella Rabinovich, Benjamin Sznajder, Artem Spector, Ilya Shnayderman, Ranit Aharonov, David Konopnicki and Noam Slonim</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1522" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1487">
                        <td>
                            <span class="poster-title">Word Sense Induction with Neural biLM and Symmetric Patterns.</span>
                            <em>Asaf Amrami and Yoav Goldberg</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1523" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1498">
                        <td>
                            <span class="poster-title">InferLite: Simple Universal Sentence Representations from Natural Language Inference Data.</span>
                            <em>Jamie Kiros and William Chan</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1524" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1541">
                        <td>
                            <span class="poster-title">Similarity-Based Reconstruction Loss for Meaning Representation.</span>
                            <em>Olga Kovaleva, Anna Rumshisky and Alexey Romanov</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1525" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1576">
                        <td>
                            <span class="poster-title">What can we learn from Semantic Tagging?.</span>
                            <em>Mostafa Abdou, Artur Kulmizev, Vinit Ravishankar, Lasha Abzianidze and Johan Bos</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1526" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1610">
                        <td>
                            <span class="poster-title">Conditional Word Embedding and Hypothesis Testing via Bayes-by-Backprop.</span>
                            <em>Rujun Han, Michael Gill, Arthur Spirling and Kyunghyun Cho</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1527" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1553">
                        <td>
                            <span class="poster-title">Classifying Referential and Non-referential It Using Gaze.</span>
                            <em>Victoria Yaneva, Le An Ha, Richard Evans and Ruslan Mitkov</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1528" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="poster-type">Semantic Parsing and Semantic Inference</span>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1410">
                        <td>
                            <span class="poster-title">When data permutations are pathological: the case of neural natural language inference.</span>
                            <em>Natalie Schluter and Daniel Varab</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1534" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1735">
                        <td>
                            <span class="poster-title">Bridging Knowledge Gaps in Neural Entailment via Symbolic Models.</span>
                            <em>Dongyeop Kang, Tushar Khot, Ashish Sabharwal and Peter Clark</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1535" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2032">
                        <td>
                            <span class="poster-title">The BQ Corpus: A Large-scale Domain-specific Chinese Corpus For Sentence Semantic Equivalence Identification.</span>
                            <em>Jing Chen, Qingcai Chen, Xin Liu, Haijun Yang, Daohe Lu and Buzhou Tang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1536" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2299">
                        <td>
                            <span class="poster-title">Interpreting Recurrent and Attention-Based Neural Models: a Case Study on Natural Language Inference.</span>
                            <em>Reza Ghaeini, Xiaoli Fern and Prasad Tadepalli</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1537" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1375">
                        <td>
                            <span class="poster-title">Towards Semi-Supervised Learning for Deep Semantic Role Labeling.</span>
                            <em>Sanket Vaibhav Mehta, Jay Yoon Lee and Jaime Carbonell</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1538" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1668">
                        <td>
                            <span class="poster-title">Identifying Domain Adjacent Instances for Semantic Parsers.</span>
                            <em>James Ferguson, Janara Christensen, Edward Li and Edgar Gonzàlez</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1539" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="1719">
                        <td>
                            <span class="poster-title">Mapping natural language commands to web elements.</span>
                            <em>Panupong Pasupat, Tian-Shun Jiang, Evan Liu, Kelvin Guu and Percy Liang</em>&nbsp;&nbsp;
                            <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1540" aria-hidden="true" title="PDF"></i>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-8">
        <span class="session-title">Mini-Break</span>
        <br/>
        <span class="session-time" title="Sunday, 4 November 2018">14:45 &ndash; 15:00</span>
    </div>
    <div class="session session-expandable session-plenary">
        <div id="expander"></div>
        <a href="#" class="session-title">
            <strong>Keynote III: "The Moment of Meaning and the Future of Computational Semantics"</strong>
        </a>
        <br/>
        <span class="session-people">
            <a href="https://www.rug.nl/staff/johan.bos/" target="_blank">Johan Bos (University of Groningen)</a>
        </span>
        <br/>
        <span class="session-time" title="Sunday, 4 November 2018">15:00 &ndash; 16:00</span>
        <br/>
        <span class="session-location btn btn--location">Gold Hall / Copper Hall / Silver Hall / Hall 100</span>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">
                <p>There are many recent advances in semantic parsing: we see a rising number of semantically annotated corpora and there is exciting technology (such as neural networks) to be explored. In this talk I will discuss what role computational semantics could play in future natural language processing applications (including fact checking and machine translation). I will argue that we should not just look at semantic parsing, but that things can get really interesting when we can use language-neutral meaning representations to draw (transparent) inferences. The main ideas will be exemplified by the parallel meaning bank, a new corpus comprising texts annotated with formal meaning representations for English, Dutch, German and Italian.&nbsp;
                    <i class="fa fa-television slides-icon" data="/downloads/keynote-slides/JohanBos.pdf" aria-hidden="true" title="Slides"></i>&nbsp;
                    <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306143088" aria-hidden="true" title="Video"></i>
                </p>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-9">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time" title="Sunday, 4 November 2018">16:00 &ndash; 16:30</span>
    </div>
    <div class="session session-expandable session-papers-best">
        <div id="expander"></div>
        <a href="#" class="session-title">Best Paper Awards and Closing</a>
        <br/>
        <span class="session-time" title="Sunday, 4 November 2018">16:30 &ndash; 18:00</span>
        <br/>
        <span class="session-location btn btn--location">Gold Hall / Copper Hall / Silver Hall / Hall 100</span>
        <br/>
        <div class="paper-session-details">
            <br/>
            <table class="paper-table">
                <tr id="best-paper" paper-id="1904">
                    <td id="paper-time">16:30&ndash;16:42</td>
                    <td>
                        <span class="paper-title">How Much Reading Does Reading Comprehension Require? A Critical Investigation of Popular Benchmarks.</span>
                        <em>Divyansh Kaushik and Zachary C. Lipton</em>&nbsp;&nbsp;
                        <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1546" aria-hidden="true" title="PDF"></i>&nbsp;
                        <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306140720" aria-hidden="true" title="Video"></i>
                    </td>
                </tr>
                <tr id="best-paper" paper-id="71">
                    <td id="paper-time">16:42&ndash;17:00</td>
                    <td>
                        <span class="paper-title">MultiWOZ - A Large-Scale Multi-Domain Wizard-of-Oz Dataset for Task-Oriented Dialogue Modelling.</span>
                        <em>Paweł Budzianowski, Tsung-Hsien Wen, Bo-Hsiang Tseng, Iñigo Casanueva, Stefan Ultes, Osman Ramadan and Milica Gasic</em>&nbsp;&nbsp;
                        <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1547" aria-hidden="true" title="PDF"></i>&nbsp;
                        <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306141298" aria-hidden="true" title="Video"></i>
                    </td>
                </tr>
                <tr id="best-paper" paper-id="1537">
                    <td id="paper-time">17:00&ndash;17:18</td>
                    <td>
                        <span class="paper-title">Linguistically-Informed Self-Attention for Semantic Role Labeling.</span>
                        <em>Emma Strubell, Patrick Verga, Daniel Andor, David Weiss and Andrew McCallum</em>&nbsp;&nbsp;
                        <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1548" aria-hidden="true" title="PDF"></i>&nbsp;
                        <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306141078" aria-hidden="true" title="Video"></i>
                    </td>
                </tr>
                <tr id="best-paper" paper-id="1195">
                    <td id="paper-time">17:18&ndash;17:36</td>
                    <td>
                        <span class="paper-title">Phrase-Based & Neural Unsupervised Machine Translation.</span>
                        <em>Guillaume Lample, Myle Ott, Alexis Conneau, Ludovic Denoyer and Marc'Aurelio Ranzato</em>&nbsp;&nbsp;
                        <i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/D18-1549" aria-hidden="true" title="PDF"></i>&nbsp;
                        <i class="fa fa-file-video-o video-icon" data="https://vimeo.com/306145842" aria-hidden="true" title="Video"></i>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div id="generatePDFForm">
        <div id="formContainer">
            <input type="checkbox" id="includePlenaryCheckBox" value="second_checkbox"/>&nbsp;&nbsp;<span id="checkBoxLabel">Include plenary sessions in schedule</span>
            <br/>
            <a href="#" id="generatePDFButton" class="btn btn--twitter btn--large">Download PDF</a>
        </div>
    </div>
</div>