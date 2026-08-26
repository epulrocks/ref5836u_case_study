# AI REFLECTION
During the development, most of the time I would just use Google Search for documentation of the module I am using, and also for quick recap of the function name and parameters, or the structure of the code. 
However, there are times AI came to the rescue and helped me during the development, especially if I need the bigger picture of code structure for specific use case that is hard to find by with a Google search, or, a quick summary of errors I am facing. I mainly use 2 AI tools which has been in my daily routine, which is Gemini and Github Copilot.

1) Gemini chat:
	- This has been my method to find answer after I failed to get results from Google Search, or, when I have something more complex to ask.
	- For some code blocks that are commonly used by me, but almost impossible to memorize.
	- For some errors that I don't understand, I usually just paste the error into the chat and it gives me suggestions on what I need to look for. Doing the same method on Google Search hardly gives me the solution on the first search. This is because Gemini understands what kind of work, or what tools we are currently using, so usually Gemini was able to give me suggestions tailored to my case.
	- For spelling check on my markdown files

2) Github Copilot:
	- This tools helps me a lot in terms of code completion.
	- I dont usually use the chat feature (as I have Gemini for that), so I did not depend on this to write the whole code.
	- Some code completion that is very helpful is when I want to write some repetitive block of code with minor different, most of the time it gave me accurate suggestion that I need.
	- It also helps on some typos that I did, it even gave the correct spelling and syntax suggestion even before I got the chance to press debug. This made development fast since I don't need to wait for a failed debug to realize my mistake

## What I delegated to AI vs. decided/wrote myself
In this project, I decide the overall process flow as this is something similar to what I have done before and I have a clear picture of what to write. I did not delegate much of the overall architecture process, but AI definitely helped me a lot in debugging process and recalling code structures. However, in other project that I am not familiar with, usually I explain the target and available resources to Gemini to get suggestion on planning the architecture.

## Where the AI was **wrong or misleading**
A few times that AI suggested me code that does not work, or maybe I did not implement it properly. One occurrence I can remember is when I wanted to silence a warning received from Gemini API module, and the code suggestion does not work. Unfortunately, I cannot determine if that suggestion from Gemini was invalid or not, as I decided not to use it anyway after realizing that the warning does not appear in log files.

## Comment on Category Classification using AI
As mentioned in README, I believe the current method of using LLM is reliable, however, it might be costly in the long run. We should try to implement our own model to classify those freetext categories instead if this automation was to be implemented in a long run.