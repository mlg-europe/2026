# Hints for the Website

This is supposed to be a very lightweight thing. 
Static site generation at its minimum, basically hand written html with generated bibliography.

to update the page, edit ```index.html_template``` and ```acceptedpapers.bib```

then, (locally), run

```
python poormans_page_generator.py
``` 

and push the changes to the repo:

```
git add *
git commit -m 'I updated the page'
git push
```


# Requirements and build

This site was built using

- [neat.css](https://neat.joeldare.com) to have very basic layout
- [bibtexparser](bibtexparser.readthedocs.org) to generate html from a bibtex file.

To install bibtexparser, use pip

```pip install bibtexparser```



# Template for bibtex

we have three relevant 'publicationtype' values: accepted, bestpaper, bestposter

```
@article{ln,
publicationtype = {accepted},
  pdf = {},
  poster = {},
  slides = {},
  video = {},
  code = {},
  reviews = {},
  venuetype = {},
  venueurl = {},
  author       = {},
  title        = {},
  year = {},
  journal = {},
  volume = {}, 
  comment = {},
}
```

```
@inproceedings{ln,
publicationtype = {accepted},
  pdf = {},
  poster = {},
  slides = {},
  video = {},
  code = {},
  reviews = {},
  venuetype = {},
  venueurl = {},
  author       = {},
  title        = {},
  year = {},
  booktitle = {}, 
  comment = {},
}
```