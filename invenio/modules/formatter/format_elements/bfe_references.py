# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011, 2014 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Prints references
"""
__revision__ = "$Id$"

def format_element(bfo, reference_prefix, reference_suffix):
    """
    Prints the references of this record

    @param reference_prefix: a prefix displayed before each reference
    @param reference_suffix: a suffix displayed after each reference
    """
    from invenio.config import CFG_BASE_URL, CFG_ADS_SITE
    from invenio.legacy.search_engine import get_mysql_recid_from_aleph_sysno, \
         print_record

    if CFG_ADS_SITE:
        ## FIXME: store external sysno into 999 $e, not into 999 $r
        # do not escape field values for now because of things like A&A in
        # 999 $r that are going to be resolved further down:
        references = bfo.fields("999C5", escape=0)
    else:
        references = bfo.fields("999C5", escape=1)
    out = ""

    for reference in references:
        ref_out = ''

        if 'o' in reference:
            if out != "":
                ref_out = '</li>'
            ref_out += "<li><small>"+ reference['o']+ "</small> "

        if 'm' in reference:
            ref_out += "<small>"+ reference['m']+ "</small> "

        if 'r' in reference:
            if CFG_ADS_SITE:
                # 999 $r contains external sysno to be resolved:
                recid_to_display = get_mysql_recid_from_aleph_sysno(reference['r'])
                if recid_to_display:
                    ref_out += print_record(recid_to_display, 'hs')
                else:
                    ref_out += '<small>' + reference['r'] + ' (not in ADS)</small>'
            else:
                ref_out += '<small> [<a href="'+CFG_BASE_URL+'/search?f=reportnumber&amp;p='+ \
                       reference['r']+ \
                       '&amp;ln=' + bfo.lang + \
                       '">'+ reference['r']+ "</a>] </small> <br />"

        if 't' in reference:
            ejournal = bfo.kb("ejournals", reference.get('t', ""))
            if ejournal != "":
                ref_out += ' <small> <a href="https://cds.cern.ch/ejournals.py?publication='\
                      + reference['t'].replace(" ", "+") \
                +"&amp;volume="+reference.get('v', "")+"&amp;year="+\
                reference.get('y', "")+"&amp;page="+\
                reference.get('p',"").split("-")[0]+'">'
                ref_out += reference['t']+": "+reference.get('v', "")+\
                       " ("+reference.get('y', "")+") "
                ref_out += reference.get('p', "")+"</a> </small> <br />"
            else:
                ref_out += " <small> "+reference['t']+ reference.get('v', "")+\
                       reference.get('y',"")+ reference.get('p',"")+ \
                       " </small> <br />"


        if reference_prefix is not None and ref_out != '':
            ref_out = reference_prefix + ref_out
        if reference_suffix is not None and ref_out != '':
            ref_out += reference_suffix

        out += ref_out

    if out != '':
        out += '</li>'

    return out

def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
