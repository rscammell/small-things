# WMLGen

**Written in Python 1.x in 2000. Unmaintained since then, but presented here for historic interest and potential usefulness.***
This software was originally released in the public domain, but I'd appreciate credit for it if you find it useful.

WMLGen simplifies the generation and management of [Wireless Markup Language](https://en.wikipedia.org/wiki/Wireless_Markup_Language) decks and cards for Python [WAP](https://en.wikipedia.org/wiki/Wireless_Application_Protocol) applications. 
The library provides a variety of functions that implement critical features of the WML spec. 
Functions implemented in this version include WML Prolog output, deck/card creation, anchor creation, image placement, and a selection of pre-formatting functions, such as single command card creation, and title printing.

A guide to some of the available functions is shown below (additional functions are documented inline within the source):

```intro_DTD()```:
Use: Prints the content type (text/vnd.wap.wml), followed by the WAP WML v1.1 DTD Prolog.
Parameters: none.
Context: This should be the first command issued when creating a WML document.
Usage example: ```intro_DTD()```

```open_wml()```:
Use: Prints the opening <wml> tag that indicates the beginning of a WML deck.
Parameters: none.
Context: This command should be issued whenever a new deck is to be created.
Usage example: ```open_wml()```

```close_wml()```:
Use: Prints the closing </wml> tag that indicates the end of a WML deck.
Parameters: none.
Context: This command should be issued whenever a WML deck is to be ended.
Usage example: ```close_wml()```

```create_card(c_id, c_title)```:
Use: Prints the opening <card> tag that creates a card within a WML deck.
Parameters: 2
```c_id```: The identifying name of the card (e.g. "main").
```c_title```: The title of the card (e.g. "Main Menu"). Note: Not all WAP browsers will display this field when the card is shown.
Context: This command should be issued whenever a new card is to be created within a WML deck.
Usage example: ```create_card("main","Main Menu")```

```close_card()```:
Use: Prints the closing ```</card>``` tag that ends a card within a WML deck.
Parameters: none.
Context: This command should be used to close a created WML card.
Usage example: ```close_wml()```

```create_anchor(a_name, a_href)```:
Use: Creates a WML anchor.
Parameters: 2
```a_name```: The name of the anchor, (e.g. "Resume")
```a_href```: The URL of the anchor, (e.g. http://wap.google.com)
Context: This command should be used to create anchors within WML cards to other cards in the local WML deck, or external WAP sites.
Usage example: ```create_anchor("Search the Web","http://wap.google.com")```

```create_text_input()```:
Use: Create a button that passes a variable within the WML deck to a specific location (e.g. a CGI script). 