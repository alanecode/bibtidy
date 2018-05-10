#! /usr/bin/env python
from __future__ import print_function
import sys
import re
import bibtexparser

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

# print sys.argv


def get_all_library_entries(bibtex_file_name):
    """Open bibtex file, return a list of dicts containing entries."""
    with open(bibtex_file_name) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        return bib_database.entries

def flatten(aList):
        t = []
        for i in aList:
            if not (isinstance(i, list) or isinstance(i, tuple)):
                t.append(i)
            else:
                t.extend(flatten(i))
        return t

def get_unique_cited_keys(tex_file_name):
    """Open provided tex file, return a list of unique citation keys."""
    r = re.compile(r'\\cite\{(.*?)\}|\\parencite\{(.*?)\}')
    citation_keys = []
    with open(tex_file_name, 'r') as tex_file:
        for line in tex_file:
            line_keys = r.findall(line)
            if line_keys:
                citation_keys.append(line_keys)
    citation_keys = flatten(citation_keys)
    citation_keys = [x.split(',') for x in citation_keys]
    citation_keys = flatten(citation_keys)
    citation_keys = list(set([x.strip() for x in citation_keys if x<>'']))
    return citation_keys
            
            
def get_list_of_cited_entries(cited_keys, all_library_entries):
    """Return a list of dicts corresponding to subset of bibtex library."""
    cited_entries = []
    for entry in all_library_entries:
        if entry['ID'] in cited_keys:
            cited_entries.append(entry)
            cited_keys.remove(entry['ID'])

    # warn if keys have been cited which aren't found in library
    for k in cited_keys:
        print('WARNING: no entry for ' + k + ' found in library')
        
    return cited_entries

def write_bib_file(list_of_cited_entries, output_fname):
    db = BibDatabase()
    db.entries = list_of_cited_entries
    writer = BibTexWriter()

    with open(output_fname, 'w') as bibtex_file:
            bibtex_file.write(writer.write(db))

    print('Output written to ' + output_fname)

if __name__ == '__main__':
    bib_file = '/home/andrew/Dropbox/phd/data/literature/library.bib'
    tex_file = '/home/andrew/Dropbox/articles/graphs-as-ecological-models/property-graphs-configure-LULC-model.tex'
    out_file = '/home/andrew/Dropbox/articles/graphs-as-ecological-models/property-graphs-configure-LULC-model.bib'

    cited_entries = get_list_of_cited_entries(get_unique_cited_keys(tex_file),
                                              get_all_library_entries(bib_file))

    write_bib_file(cited_entries, out_file)



    

