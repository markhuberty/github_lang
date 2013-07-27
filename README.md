Analyzing language use on Github
=======================


[Redmonk](http://redmonk.com/sogrady/2013/07/25/language-rankings-6-13/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+tecosystems+%28tecosystems%29), building on [work](http://www.dataists.com/2010/12/ranking-the-popularity-of-programming-langauges/) by Drew Conway and John Myles White, publishes regular data on language popularity. The data come from Github and StackOverflow. 

That analysis tracks popularity. It got me thinking about complementarity--what languages go together? We can think of that in one of two ways: 

1. How do languages compare in terms of the problems they solve?
2. What languages do users themselves pick up together? 

We can exploit Github and StackOverflow data to study this as well. 


User complementarity
----------

Do C and Java go together? What about Javascript and Assembler? To answer this question, we can observe what people use in the real world. To study this, I pulled the [Github repository data](http://archive.org/details/archiveteam-github-repository-index-201212) for over a million repositories that the folks at the Internet Archive scraped in December 2012. From that data, the Github API allows us to query what languages show up in each user's repository. From that data, I build a user:[languages] map.


Task complementarity
--------------

Languages are ultimately tools, though, and tools help solve problems. Hence we'd like to know how tools group together based on the tasks they solve. Here, StackOverflow provides some valuable data. Each question on StackOverflow gets a set of tags, which usually include both the programming language(s) covered in the question, and the problem the question is trying to solve. For example, a question might be tagged (`C`, `sorting`), while another question might be tagged (`Java`, `sorting`). That's a trivial example, but it gets to the point: a question usually revolves around a *tool* and a *task*. We can think of the tasks as bridges between tools. Languages are complementary to the extent they help solve the same tasks. 

We can compute the task relations relatively simply: for two tags `T` and `T*`, compute the complementarity as *max* (P(`T` | `T*`), P(`T*` | `T`)). Why *max*? Consider the tags "unix" and "bash". P("bash" | "unix") ~ 0 (there's a lot of stuff tied to unix, of which bash is only one small part), while P("unix" | "bash") ~ 1. Using the max helps to maintain the structure of pairwise tag relations that we expect.  



