#!/usr/bin/python
#
# splashid_to_keepass.py - convert SplashID export to KeePass import
#
# Ch. Bueche <bueche@netnea.com>
# 23.9.2013 : initial version
#
# ------------------------------------------------------------------------------------------
# installation and usage : https://github.com/cbueche/splashid2kepass
# ------------------------------------------------------------------------------------------


from optparse import OptionParser
import os.path
import unicodecsv
import sys
import time
import csv

# -----------------------------------------------------------
# main
# -----------------------------------------------------------

parser = OptionParser()
parser.add_option("-i", "--input-file",  dest  ="input_file", default="", help="input file")
parser.add_option("-o", "--output-file", dest ="output_file", default="", help="output file")
(options, args) = parser.parse_args()

if os.path.isfile(options.input_file):
	pass
else:
	print "Cannot find input file"
	sys.exit(1)

# read exported CSV

entries = []
with open(options.input_file, 'rU') as csvfile:

	reader = unicodecsv.reader(csvfile, encoding='MACROMAN')
	try:
		for row in reader:
			if row[0] == 'SplashID Export File':
				continue
			# print 'DECODED : ', ', '.join(row)
			entry = {}
			entry['type']        = row[0]
			entry['description'] = row[1]
			entry['username']    = row[2]
			entry['password']    = row[3]
			entry['url']         = row[4]
			entry['f5']          = row[5]
			entry['f6']          = row[6]
			entry['f7']          = row[7]
			entry['f8']          = row[8]
			entry['f9']          = row[9]
			entry['modified']    = row[10]
			entry['notes']       = row[11]
			entry['category'] = row[12]
			entries.append(entry)
	except csv.Error as e:
		sys.exit('file %s, line %d: %s' % (options.input_file, reader.line_num, e))

# write import CSV for KeePass

with open(options.output_file, 'w') as csvoutput:

	writer = unicodecsv.writer(csvoutput, encoding='utf-8')

	# header
	writer.writerow(('Description', 'Username', 'Password', 'URL', 'Modified', 'Notes', 'Category'))

	for entry in entries:

		# format date in something easier to import
		entry['modified'] = time.strftime("%Y-%m-%dT00:00:00", time.strptime(entry['modified'], "%B %d,%Y"))

		# fields 5 to 9 are better at end of notes than in their own attributes
		for field in ['f5', 'f6', 'f7', 'f8', 'f9']:
			# print "field %s : <%s>" % (field, entry[field])
			if entry[field] is None or entry[field] == '' or entry[field] == ' ':
				pass
			else:
				entry['notes'] += "\n"
				entry['notes'] += entry[field]

		# output the new CSV record
		writer.writerow((	entry['description'],
							entry['username'],
							entry['password'],
							entry['url'],
							entry['modified'],
							entry['notes'],
							entry['category']
							))

print "%s records converted" % (len(entries))
print "conversion done. Be sure to delete your temporary files after successful import into KeePass"
