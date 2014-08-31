# -*- coding: utf-8 -*-

"a helper module used by tsv2vw"

import json
import pdb
import re
def get_words( text ):
    return text.replace( '|', ' ' ).replace( ':', ' ' ).replace( "\n", ' ' ).replace( ',', ' ' ).replace( '.', ' ' ).replace('/', ' ')

def construct_line( line ):
    
    new_line = []

    try:
        label = line['is_blocked']
    except KeyError:
        # test
        label = '1'
        
    if label == '0':
        label = '-1'
        
    new_line.append( "{} 1 {}|i".format( label, line['itemid'] ))
    
    # integer features: |i namespace
    for c in ( 'price', 'phones_cnt', 'emails_cnt', 'urls_cnt' ):
        v = line[c]
        new_item = "{}:{}".format( c, v )
        new_line.append( new_item )
        
    # |c and |s namespaces    
    for c in ( 'category', 'subcategory' ):
        v = line[c].replace( ' ', '_' )
        new_item = "|{} {}".format( c[0], v )
        new_line.append( new_item )        
    
    # |t and |d namespaces
    for c in ( 'title', 'description' ):
        v = get_words( line[c] )
        new_item = "|{} {}".format( c[0], v )
        new_line.append( new_item )    
    
    attrs = None
    if line['attrs'] != '':
        try:    
            attrs = json.loads( line['attrs'] )
        except ValueError:    
            try:
                #pdb.set_trace()
                attrs = json.loads(re.sub('/\"(?!(,\s"|}))','\\"',line['attrs']).replace("\t"," ").replace("\n"," ")) if len(line['attrs'])>0 else {}
                #attrs = json.loads( line['attrs'].replace( '/"', r'\"' ))
            except ValueError:
                #pdb.set_trace()
                print "json.loads() failed, trying eval()..."
                #print line['attrs']
                #try: 
                    # will produce UnicodeDecodeError below
                #    print line['attrs'].replace( '/"', r' ' )
                #    print "runhere"
                    #attrs = eval( line['attrs'] )
                    #print "OK"
                #except ValueError:
                    #print str(line['attrs'].replace( '/"', r' ' ))
                 #   print "error"
    
    if attrs:
        attribs = []
        for k, v in attrs.items():
            attribs.append(( k + '_' + v ).replace( ' ', '_' ).replace( ':', '_' ))
            
        try:
            attribs = map( lambda x: x.encode( 'utf-8' ), attribs )
        except UnicodeDecodeError:
            pass
            # print "UnicodeDecodeError"
        
        #print attribs
        new_item = "|a {}".format( " ".join( attribs ))
        new_line.append( new_item )            
        
    new_line = " ".join( new_line )
    new_line += "\n"
    return new_line
