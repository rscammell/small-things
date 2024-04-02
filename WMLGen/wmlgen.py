#!/usr/local/bin/python

#--------------------------------------------------------------
# WMLGen v. 0.03b
# A module that provides simple WML tag generation functions to
# simplify WAP WML application development.

# Authors: Rupert Scammell (rupe@metro.yak.net), Alexey N. Shirkoff (alexis@rosnet.ru)
# Date: 8.17.2000
# Version:  0.03b
# Parnassus: http://www.vex.net/parnassus/apyllo.py/812237977.281773030.91251116

# Version History:
# 0.01a, 06.06.2000. Initial version.
# 0.02a, 06.13.2000. Added closing </go> tag in create_anchor() function.
# 0.02a, 06.13.2000. Added additional documentation to functions.
# 0.03b, 08.17.2000. Cyrillic Windows 1251 -> Unicode conversion, timer card,
# template functionality added by Alexey N. Shirokoff (alexis@rosnet.ru)

#---------------------------------------------------------------

import sys

# print the initial WAP WML DTD Prolog

def intro_DTD():
	print 'Content-type: text/vnd.wap.wml'
# Here in case we want to debug using a browser
#	print 'Content-type: text/plain'
	print
	print '<?xml version="1.0"?>'
	print '<!DOCTYPE wml PUBLIC "-//WAPFORUM/DTD WML 1.1//EN" "http://www.wapforum.org/DTD/wml_1.1.xml">'

# print the opening WML tag
def open_wml():
	print '<wml>'

# print the closing wml tag
def close_wml():
	print '</wml>'

# create a card with id and title attributes
# c_id = card id
# c_title = card_title
def create_card(c_id, c_title):
	print '<card id="' + c_id + '" title="' + c_title + '">'

# close the card
def close_card():
	print '</card>'

# create timer card	
# c_id = card id
# on_timer = document to go to after time expires
# title = Optional parameter specifying a title to use for
# the timer card.
# pause_time = Time ( in 10ths of a second) to wait, e.g. 30 = 3 seconds.

def create_timer(c_id, on_timer, pause_time, title=None):
	if title:
		print '<card id="' + c_id + '" title="'+title+'" ontimer="#' + on_timer + '">'
	else:
		print '<card id="' + c_id + '" ontimer="#' + on_timer + '">'
	print '<timer value="'+str(pause_time)+'"/>'

# create template
# temp_dict i.e {'type':['name','label','href'], 'type':['name','label'], 'type':'', 'type':None} 
# where the type is go|prev|noop|refresh

def create_template(temp_dict):
	print '<template>'
	for i in temp_dict.keys():
		if temp_dict[i] in ['', None, []]:
			print '<do type="'+i+'">'
		else:
			print '<do type="'+i+'" name="'+temp_dict[i][0]+'" label="'+temp_dict[i][1]+'">'
		if type == 'go':
			print '<'+i+' href='+temp_dict[i][2]+'/></do>'
		else:
			print '<'+i+'/></do>'
	print '</template>'

#convert Cyrillic Windows-1251 characters into unicode
# r_string = A string of Cyrillic Windows-1251 characters to convert to unicode
# returns nr_string = A string of unicode CW-1251 characters.

def uniesc(r_string=None):
	if not r_string:
		return ''
	suff = '&#x'
	alpha = {'À':'0410', 'Á':'0411', 'Â':'0412', 'Ã':'0413', 'Ä':'0414', 'Å':'0415', '¨':'0415', 'Æ':'0416', 'Ç':'0417', 'È':'0418', 'É':'0419', 'Ê':'041A', 'Ë':'041B', 'Ì':'041C', 'Í':'041D', 'Î':'041E', 'Ï':'041F', 'Ð':'0420', 'Ñ':'0421', 'Ò':'0422', 'Ó':'0423', 'Ô':'0424', 'Õ':'0425', 'Ö':'0426', '×':'0427', 'Ø':'0428', 'Ù':'0429', 'Ú':'042A', 'Ü':'042C', 'Ý':'042D', 'Þ':'042E', 'ß':'042F', 'Û':'042B', 'à':'0430', 'á':'0431', 'â':'0432', 'ã':'0433', 'ä':'0434', 'å':'0435', '¸':'0435', 'æ':'0436', 'ç':'0437', 'è':'0438', 'é':'0439', 'ê':'043A', 'ë':'043B', 'ì':'043C', 'í':'043D', 'î':'043E', 'ï':'043F', 'ð':'0440', 'ñ':'0441', 'ò':'0442', 'ó':'0443', 'ô':'0444', 'õ':'0445', 'ö':'0446', '÷':'0447', 'ø':'0448', 'ù':'0449', 'ü':'044C', 'ú':'044A', 'û':'044B', 'ý':'044D', 'þ':'044E', 'ÿ':'044F', }
	from cgi import escape
	r_string = escape(r_string, 1)
	nr_string = ''
	for i in range(0, len(r_string)):
		if ord(r_string[i]) > 128:
			nr_string = nr_string+suff+alpha[r_string[i]]+';'
		else:
			nr_string = nr_string+r_string[i]
	return nr_string

# create an anchor
# a_name = anchor name
# a_href = anchor url
def create_anchor(a_name, a_href, a_title=None):
	if title:
		print '<anchor title="'+title+'">' + a_name
	else:
		print '<anchor>' + a_name	
	print '<go href="' + a_href + '">'
	print '</go>'
	print '</anchor>'

# create text input field
# ti_label = Action displayed, e.g. "Submit"
# ti_loc = Location to which the data is being passed, e.g.
# http://www.my.com/cgi-bin/myscript.py?variable=$(varname)
def create_text_input(ti_label, ti_loc):
	print '<do type="accept" label="' + ti_label + '">'
	print '<go href="' + ti_loc + '"/>'
	print '</go>'
	print '</do>'


# print text_input field
# ti_var = The variable data to accept (e.g. varname)
# ti_type = The type of text input, e.g. 1 for text, 2 for password type
def print_text_input(ti_type, ti_var, ti_value=None):
	ti_types = {1:'text',2:'password',3:'hidden'}
	if value:
		print '<input type="'+ ti_types[ti_type] +'" name="' + ti_var + '" value="'+ ti_value +'"/>'
	else:
		print '<input name="' + ti_var + '"/>'

# create an image
# i_name = The image name (e.g. myimg.wbmp)
# i_alt = Alternate text, in case the image can't be displayed.
# i_center = center image, if true
def create_img(i_name, i_alt, i_center=None):
	if i_center:
		print '<p align="center">'
	print '<img src="' + i_name + '" alt="' + i_alt + '"/>'
	if i_center:
		print '</p>'


# simple card creation function
# sc_id: card id name
# sc_title: card title (in bold)
# sc_text: block text to format
# sc_link_name: a link name at the bottom of the card
# sc_link_href: link location at the bottom of the card
# 
# The card will look like:
#
# ------------------------
# | Bold Title Here      | <--- sc_title
# |		      	 |
# | text text text text  | <--- sc_text
# |  text text text text | <
# | text text text text  | <
# |                      |
# | <Page Link>          | <--- sc_link_name
# -----------------------

def simple_card(sc_id,sc_title,sc_text,sc_link_name,sc_link_href):
	create_card(sc_id,sc_title)
	print '<p>'
	print '<b>' + sc_title + '</b>'
	print '</p><p>'
	print sc_text
	print '</p><p>'
	create_anchor(sc_link_name, sc_link_href)
	print '</p>'
	close_card()

# print a title in bold, with separation:
# p_title: text to print 
def print_title(p_title):
	print '<p><b>' + p_title + '</b></p>'
	print '<br/>'

# Create a radio button menu:
# bm_name: menu name
# bm_table: A Python dictionary containing key/value pairs,
# where the keys represent the option values, and the associated
# values are strings containing the menu item names.

def create_button_menu(bm_name, bm_table):
	# Get a list of the keys we've been passed
	menu_keys = bm_table.keys()
	# How many keys?
	menu_len = len(menu_keys)
	
	print '<select name="' + bm_name + '">'
	for i in range(menu_len):
		print '<option value="' + menu_keys[i] + '">' +\
		bm_table[menu_keys[i]] + '</option>'
	print '</select>'