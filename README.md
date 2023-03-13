# Book status for profile README

This project provides a badge for sharing your current book in your github profile.

<p align="center">
  <img src="https://goodreads-readme.vercel.app/api/book" alt="GoodReads"/>
</p>


It is heavily inspired by [spotify-readme](https://github.com/novatorem/spotify-readme).  

## Set Up Guide

- Go to your goodreads profile (on your PC).
- Next to "Your recent updates" there is an hyperlink called **rss**
- Note down the 8 digit integer in the ending of the URL's path section
- Add the following into the readme file, replacing the parameter with the id
    you noted down.

```
<h3 align="left">I am currently reading:</h3>
<a href="<Your Profile URL>"><img src="https://goodreads-readme.vercel.app/api/book?id=<ID you noted down>" alt="GoodReads reading" width="350" /></a>
```

