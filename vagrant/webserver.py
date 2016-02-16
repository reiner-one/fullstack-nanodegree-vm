# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import db_anfragen
import re

header ='''<html lang="de">
	<head><meta charset="utf-8"></head><body>'''
footer = '''</body></html>'''
new_form = '''<form method="POST" enctype="multipart/form-data"
	action="/restaurants/new"><h2>Wie soll das neue Restaurant heißen?</h2>
	<input name="message" type="text" ><input type="submit" value="Senden">
	</form>'''
back = '<a href="/restaurants">zurück zur Übersicht</a>'

class WebServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith("/restaurants"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = header
			restaurants = db_anfragen.getAllRestaurants()
			for restaurant in restaurants:
				output += restaurant.name.encode("utf-8") + "<br>"
				output += '''<a href="restaurants/%s/edit">Bearbeiten</a>
				 <a href="restaurants/%s/delete">Löschen</a>
				 <br><br>''' % (restaurant.id,restaurant.id)
			output += '<a href="/restaurants/new">Neues Restaurant hinzufügen</a>'
			output += footer
			self.wfile.write(output)
			return
		elif self.path.endswith("/restaurants/new"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = header + new_form + footer
			self.wfile.write(output)
			return
		elif self.path.endswith("/edit"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			restaurant = getPathID(self.path)
			output = header
			output += '''<form method="POST" enctype="multipart/form-data"
	action="/restaurants"><h2>Restaurant %s umbenennen in:</h2>
	<input name="message" type="text" >
	<input name="message" type="text" value="%s" style="display:none">
	<input type="submit" value="Senden">
	</form>''' % (restaurant.name,restaurant.id)
			output += footer
			self.wfile.write(output)
			return
		elif self.path.endswith("/delete"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			restaurant = getPathID(self.path)
			output = header
			output += '<h2>Restaurant "%s" wirklich löschen?</h2>' % restaurant.name.encode("utf-8")
			output += '''<form method="POST" enctype="multipart/form-data"
	action="/restaurants/%s/delete">
	<input name="message" type="text" value="%s" style="display:none">
	<input type="submit" value="Endgültig löschen">
	</form>''' % (restaurant.id,restaurant.id)
			output += footer
			self.wfile.write(output)
			return
		else:
			self.send_error(404, 'File not found: %s' % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()

			ctype, pdict = cgi.parse_header(
				self.headers.getheader('Content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				print fields
				messagecontent = fields.get('message')

			if self.path.endswith("/restaurants/new"):
				db_anfragen.create_restaurant(messagecontent[0])
				output = header
				output += "<h3>Neues Restaurant erstellt: %s</h3>" % messagecontent[0]
				output += "<h2>Möchtest Du ein weiteres Restaurant erstellen?</h2>"
				output += new_form + back + footer
				self.wfile.write(output)
			elif self.path.endswith("/delete"):
				restaurant_alt = db_anfragen.getRestaurant(messagecontent[0])
				alt = restaurant_alt.name.encode("utf-8")
				db_anfragen.deleteRestaurant(messagecontent[0])
				output = header
				output += '<h3>Restaurant "%s" gelöscht</h3>' % alt
				output += back
				self.wfile.write(output)
			if messagecontent[1]:
				restaurant_alt = db_anfragen.getRestaurant(messagecontent[1])
				alt = restaurant_alt.name.encode("utf-8")
				db_anfragen.updateRestaurant(messagecontent[0], messagecontent[1])
				output = header
				output += '<h3>Restaurant "%s" umbenannt in: %s</h3>' % (alt,messagecontent[0])
				output += back
				self.wfile.write(output)
		except Exception, e:
			raise e

def getPathID(pfad):
	# Extract ID
	print pfad
	m = re.search(r'restaurants\/(\d+)\/', pfad)
	return db_anfragen.getRestaurant(int(m.group(1)))

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), WebServerHandler)
		print 'Web Server läuft auf Port %s' % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, Webserver wird gestoppt"
		server.socket.close()

if __name__ == '__main__':
	main()
