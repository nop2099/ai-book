# Episode: I Want a Podcast — Part Two: Make It Secure

The security thread, error handling, TDD, and teaching someone else. Dry mix.

## Voice Design Notes

### Cast

| Tag | Voice | Draft Voice | Why |
|---|---|---|---|
| JAMES | James Wilson (clone) | Daniel | Author. |
| RICH | — | Rishi | The user. |
| OCTOPUS | — | Tessa | Claude Code. |
| PARROT | — | Karen | ChatGPT free. |
| CRAB | — | Moira | Co-Work. |
| STAGE | Samantha | Samantha | Transitions. |
| ERROR | — | Fred | Error messages. |

### Assembly overrides

- **Dry mix.** No effects.

## Script

> **Cold open**: Prepend `cold-open.md` before this script.

[JAMES]
This is I Want a Podcast, part two — make it secure. Rich has a podcast on his phone. It works. But anyone who finds the page can listen. This part is about fixing that — and it's the part that matters most. Here we go.

---
[STAGE]
Now let's talk about security. Making it secure.

[RICH]
I want a password on it.

[OCTOPUS]
Done. I put a password prompt on the page. Try it — open the U.R.L., you'll see a password box. Type the password, the player appears.

[RICH]
OK that works. But... if someone looked at the page source, could they find the audio file?

[OCTOPUS]
Yes. The filename is right there in the H.T.M.L..

[RICH]
That's not good enough.

[PARROT]
I would have done the same thing, by the way. Password div on top. And I would have been just as wrong. The correction is identical — you push back, I rethink. The only difference is when I write the fix, you'd copy it out of the chat and save it over the old file. But the thinking? Same thinking.

[OCTOPUS]
OK. I can randomize the filename — make it a long string of random characters so nobody could guess the U.R.L..

[RICH]
But it's still in the source code. If someone opens the H.T.M.L. and reads it, the filename is right there. Random or not.

[OCTOPUS]
You're right. What if I encrypt the filename with your password? The H.T.M.L. only has the encrypted version — it looks like gibberish. When you type the right password, the page decrypts the filename, loads the audio. Wrong password — you don't even know what file to ask for.

[RICH]
Now we're talking. So someone could look at the source and they'd see... what?

[OCTOPUS]
A blob of encrypted text. Meaningless without the password. The filename, the script text — all encrypted. The password never leaves your browser. It's not stored anywhere. It's used once, in your browser, to unlock the names.

[RICH]
OK. I like that.

[PARROT]
I would have gotten here too. Same four steps — password div, random name, still in source, encrypt the name. Same reasoning. Same code. The A.E.S. 256 encryption I'd write is identical to what the octopus wrote. Security is a conversation, not a command. It doesn't matter which agent you're talking to. It matters that you pushed back when the answer felt thin.

[STAGE]
Four sip tests. Four versions of the security model. Each one better than the last. Rich didn't study encryption. He didn't read a textbook. He sipped, reacted, pushed back, and the system improved. The first version was wrong. The second was better. The third was close. The fourth was right. He can now explain why it's secure — not because he memorized an answer, but because he lived the reasoning.

---

[STAGE]
Something is going to break. When something breaks.

[RICH]
OK so I deployed it, I opened it on my phone, I typed the password, and... nothing happened. The player didn't appear.

[ERROR]
Uncaught DOMException. The operation failed because the requested object could not be found.

[OCTOPUS]
Let me check. One second. OK, I see the issue — the encryption key derivation is using a different iteration count than the decryption. I wrote one number when I encrypted and a different number when I built the page. My mistake. Fixing it now. Redeploying. Try again.

[RICH]
That works now.

[PARROT]
So here's where we're really different. When something breaks with the octopus, you say "it's broken" and the octopus looks at the error, finds the bug, fixes it, redeploys, and says "try again." You waited maybe thirty seconds. With me, the same error happens, but I can't see it. I'd say "can you open the browser console and tell me what error you see?" You'd say "how do I do that?" I'd walk you through pressing F12. You'd read me the error.

[ERROR]
Uncaught DOMException. The operation failed because the requested object could not be found.

[PARROT]
You'd paste that to me. I'd read it, figure out the fix, write the corrected code, and you'd copy it into the file and redeploy. Same fix. Same understanding of what went wrong. But it took five round trips instead of one. That's the friction difference with errors — the octopus can look at the crash site itself. I need you to describe the crash site to me.

[CRAB]
When something breaks for me, it's a different flavor of frustration. I can see the error. I can read the code. I can probably even fix it. But if the fix requires installing a tool, or accessing a file outside my sandbox, or running a system command — I hit the wall. I tell you "I can't do that" and I stop. I don't try to work around it. That's the right behavior — you don't want me probing for holes in the sandbox. But it means you get a fix that's ninety percent done and you have to carry it the last mile.

[RICH]
Wait. How do I know it's actually fixed? You just said "fixing it now, redeploying." But did you check?

[OCTOPUS]
...I deployed the change.

[RICH]
But did you test it? Did you try the wrong password and make sure it fails? Did you try the right password and make sure it works? Did you try viewing the source and make sure the filename is still encrypted?

[OCTOPUS]
No. I assumed —

[RICH]
Don't assume. Show me.

[OCTOPUS]
OK. Testing now. Wrong password — page shows nothing. Correct. Right password — player appears, audio plays. Correct. View source — filename is encrypted gibberish. Correct. It works.

[RICH]
Now I believe you.

[STAGE]
Most agents skip this step. They fix the thing and say "done." They don't reproduce the error first. They don't verify the fix after. Rich doesn't know what test-driven development is. He doesn't need to. He just said the instinctive version: "Prove it works before you tell me it's fixed." That's the conductor catching a wrong note. The oboe player says "I fixed it." The conductor says "Play the passage again. Let me hear it."

[PARROT]
Same thing with me, by the way. I'd say "I fixed the code, here's the updated version." You should say "Walk me through what happens now. Wrong password — what do I see? Right password — what loads? Source code — what's visible?" Make me prove it in words before you paste the code into the file. If I can't explain why it works, the fix might not work.

[CRAB]
And with me — I can actually run some of those tests inside the sandbox. I can open the H.T.M.L. file, try the wrong password, check the result. But I might not think to do it unless you ask. Say "test it first." Two words. Changes everything.

[STAGE]
The best path — the one most agents skip — is this: reproduce the error. Make it fail on purpose. Then make the change. Then run the same test. If it passes, great. If it doesn't, undo the change and try again. Rich doesn't know that's called test-driven development. He just knows he wants to see it break and then see it work. That instinct is worth more than knowing the name.

---

[STAGE]
The build is done. Now Rich explains what he built.

[RICH]
OK so James said I have to explain it. Here goes. When someone visits the page, they see a password box. Nothing else. If they view the source code, they see encrypted blobs — the audio filename and the script are both encrypted with my password. Without the password, you can't even figure out what file to ask the server for. The password isn't stored anywhere — it's used in my browser, right there on my phone, to decrypt the filename. Then the browser asks the server for that file. If you don't know the name, you can't ask for it. And the name is random, so you can't guess it either.

[RICH]
Is that right?

[STAGE]
He explained it. In his own words. Without looking at notes. That's the test. Not a quiz. Not a grade. Can he tell someone else why it works? He can. The understanding came from the corrections, not from a lesson.

---

[STAGE]
Let's step back. What you just did.

[RICH]
I started with "I want a podcast." I didn't pick anything. I didn't know what edge T-T-S was. I didn't know what hosting service the agent would choose. I didn't know what A.E.S. 256 was. I just kept saying what I wanted and pushing back when something felt wrong.

[RICH]
One more thing. When you made the audio — you said "here's your MP3." But I don't want to open a file in Apple Music. I want to see it in my browser. With the script next to it. And a play button. And a download button.

[OCTOPUS]
I can build that. One H.T.M.L. page. Audio player at the top, transcript below, download link. Open it in your browser. Done.

[RICH]
Do it.

[CRAB]
I can write that page into the podcast folder. You'd double-click it to open in your browser. Same page, same player, same transcript.

[PARROT]
I can write the H.T.M.L. for you. You'd save it as a file and open it. More steps. Same result.

[STAGE]
"Do it." Two words. Rich didn't ask how to build an H.T.M.L. page. He didn't ask what a web player is. He said what he wanted — see it in my browser — and told the agent to make it happen. That's the "you do it" pattern. The agent is not an advisor. It's an operator. When you know what you want, say "do it" and let the agent figure out the how.

[OCTOPUS]
And now you have a settings file in your podcast folder. Next time you come here and say "make me a podcast," I already know everything — the voice, the hosting, the password scheme. I read the settings and we skip straight to the script. You taught me once. It works forever.

[PARROT]
With me, it's a little different. I can't save a settings file to your folder automatically. But I remember our conversation. And if you save the chat — most platforms let you — you have the same thing. A record of every decision. Next time you say "make me a podcast," I ask: same setup? You say yes. We skip to the script. Not as automatic. But the knowledge persists.

[STAGE]
He built a skill without trying to build a skill. The settings file — or the saved conversation — is the residue of every correction he made. The voice he chose. The hosting he chose. The encryption he pushed for. It's not a configuration file. It's a record of taste. Next time starts from where this time ended.

---

[STAGE]
Now the real question. Teaching someone else.

[RICH]
Wait. If I had to do this whole thing again from scratch — no workbook, no instructions, just me and an agent — what would I say?

[OCTOPUS]
Exactly what you said the first time. "I want a podcast."

[RICH]
That's it? But I didn't know about encryption, or hosting, or any of that.

[OCTOPUS]
You didn't need to. You said what you wanted. I asked questions. You answered honestly. When something felt wrong you said so. The encryption came from you pushing back on the security, not from you knowing the word A.E.S.. The hosting came from you saying "my phone" and "Mike too." Every requirement emerged because you reacted to what was in front of you.

[RICH]
So the prompt is just... the want.

[OCTOPUS]
The want is the prompt. Everything else is the conversation.

[RICH]
But now I know what I want. Like, all of it. If I started over, I could say it all up front. Not the technology — I don't care about that. But the requirements. The real ones. Could I just... say all of that?

[OCTOPUS]
Try it.

[RICH]
OK. "I want a personal podcast about my life. I want to listen to it on my phone. I want a password on it — and I mean really secure, like if someone looks at the source code they still can't find the audio file. No subscriptions — free tiers only. I want it to remember how I like it so next time I just say 'make me another one' and it works. And ask me about my life first before you write anything."

[OCTOPUS]
That's a perfect prompt. Every requirement is there. Not one technology choice. You told me what, not how. I'll pick the how.

[PARROT]
Same prompt works for me, word for word. I'd make different technology choices — web tools instead of command line tools — but I'd hit every requirement. Because the requirements are about what you want, not what tools to use.

[STAGE]
Two valid approaches. The stingy prompt — four words, let the conversation find the shape. And the loaded prompt — every requirement, zero technology. The stingy version teaches you what you want through the corrections. The loaded version uses what you already learned. Both arrive at the same place. The difference is whether you're discovering the requirements or stating them. After the first time, you'll always have the loaded version. Because you lived the stingy one first.

[RICH]
So how do I teach Mike to do this?

[OCTOPUS]
One sentence.

[RICH]
One sentence?

[OCTOPUS]
"Open whatever AI you have — whatever's free. Say 'I want a personal podcast, talk to me about my life, write a script, make audio I can listen to on my phone, put a password on it so only I can hear it, and make sure it's really secure — like, if someone looks at the code, they still can't find the audio.' Then have the conversation. Push back when something feels wrong."

[RICH]
That's it?

[OCTOPUS]
That's it. The prompt is the seed. The corrections are the learning. The security explanation is the proof.

[CRAB]
Works with me too. I'd build most of it — the files, the H.T.M.L., the encryption code — all saved directly into the folder. Then I'd write a little deploy script for the part I can't do. Mike runs one command. Done.

[PARROT]
And it works with me. Same sentence. ChatGPT, Gemini, Claude in a browser — doesn't matter. More copy-pasting. Same thinking. Same destination. Mike ends up with the same encrypted podcast, able to explain the same security model. The tool doesn't matter. The pushback does.

[RICH]
Huh. OK.

[STAGE]
He arrived with a want. He leaves with a system, a security model he can explain, and a sentence he can hand to someone else. The conversation was the curriculum. The corrections were the learning. The explanation was the proof. And the next person starts from the same sentence and walks their own path to the same place.

---

[STAGE]
No parrots, octopuses, crabs, or childhood dogs were harmed in this production. The sip test was conducted ethically. The encryption was real. The parrot would like you to know she can do everything the octopus can do — it just takes more trips. The crab would like you to know she can do ninety percent of what the octopus can do — she just can't reach the top shelf.

[JAMES]
That's part two — make it secure. Four corrections from password to encryption. In part three: Rich extends it with email, calendar, and spreadsheets. Thanks for listening.
