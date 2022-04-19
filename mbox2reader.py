#!/usr/bin/env python

# mbox2reader.py - given a few configurations, read an mbox file, and output a file system amenable to the Reader

# Eric Lease Morgan <emorgan@nd.edu>

# January 5, 2022 - first cut


# configure
MBOX      = './code4lib-2011.mbox'
DIRECTORY = './code4lib-2011'
MONTHS    = { 'jan':'01_jan', 'feb': '02_feb', 'mar':'03_mar', 'apr':'04_apr', 'may':'05_may', 'jun':'06_jun', 'jul':'07_jul', 'aug':'08_aug', 'sep':'09_sep', 'oct':'10_oct', 'nov':'11_nov', 'dec':'12_dec', }
TEMPLATE  = 'code4lib-##ITEM##-##DATE##.txt'
COLUMNS   = [ 'file', 'author', 'title', 'date' ]
METADATA  = 'metadata.csv'

# require
import mailbox
import pandas as pd
import sys

# initialize
unicodeErrors   = 0
attributeErrors = 0
typeErrors      = 0 
records         = []

# get and process each email message
messages = mailbox.mbox( MBOX )
for index, message in enumerate( messages ) :
		
	# parse
	author  = message[ 'from' ]
	subject = message[ 'subject' ]
	date    = message[ 'date' ]

	# continue parsing
	try :
	
		# get the body of the message; imperffect
		body = message.get_payload( decode=True )

	except AttributeError     : pass		
	except UnicodeDecodeError :  pass

	# do the hard work
	try :
		
		# get the date
		month = MONTHS[ date.split()[ 2 ].lower() ]

		# get the domain
		domain = author.split( '@' )[ 1 ].lower()
		domain = domain.replace( '>', '' )
		
		# get the title
		title = subject.replace( '[CODE4LIB] ', '' )
		
		# debug
		sys.stderr.write( '     item: ' + str( index + 1 ) + '\n' )
		sys.stderr.write( '   author: ' + author + '\n' )
		sys.stderr.write( '  subject: ' + subject + '\n' )
		sys.stderr.write( '     date: ' + date + '\n' )
		sys.stderr.write( '\n' )
		sys.stderr.write( '   domain: ' + domain + '\n' )
		sys.stderr.write( '    title: ' + title + '\n' )
		sys.stderr.write( '     date: ' + month + '\n' )
		sys.stderr.write( '  ' + str( body.decode() ) + '\n' )
		sys.stderr.write( '\n' )
		
		# configure output, and... output
		output = TEMPLATE.replace( '##ITEM##', str( index ).zfill( 4 ) )
		output = output.replace( '##DATE##', month )
		with open( DIRECTORY + '/' + output, 'w' ) as handle : handle.write( str( body.decode() ) )
		
		# update the records
		records.append( [ output, domain, title, month ] )
		
	except UnicodeDecodeError :
		unicodeErrors   += 1
		pass
	except AttributeError : 
		attributeErrors += 1
		pass
	except TypeError : 
		typeErrors      += 1
		pass

# debug
sys.stderr.write( '    unicode errors: ' + str( unicodeErrors ) + '\n' )
sys.stderr.write( '  atributre errors: ' + str( attributeErrors ) + '\n' )
sys.stderr.write( '       type errors: ' + str( typeErrors ) + '\n' )

# output metadata file and done
metadata = pd.DataFrame( records, columns=COLUMNS)
metadata.to_csv( DIRECTORY + '/' + METADATA, index=None )
exit()
