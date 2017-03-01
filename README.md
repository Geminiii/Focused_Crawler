# Focused_Crawler

##Introduction
This is a primitive focused crawler in Python that attempts to crawl web pages on a particular topic. Given a query(a set of keywords) and a number **_n_** provided by a user, the crawler would contact a Google search engine API and get the top-10 results for this query, called the **starting pages**. Then the crawl from the starting pages using a **focused strategy** until a total of n pages being collected, with most of these pages being relevant to the query/topic. Each page would be crawled only once, and stored in a file. 
##How it works

##Output
Your program should output a list of all visited URLs, in the order they are visited, into a file, together with such information such as the size of each page, the depth of each page (distance from the start pages), and whether the page was relevant.
