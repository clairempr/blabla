# Chat like a pirate!
import random
from functools import reduce


def chat_like_a_pirate(old_chat):
    new_chat = replace(old_chat)

    last_char = old_chat[-1]
    if last_char in ("?", ".", "!"):
        punc = last_char
        new_chat = new_chat[:-1]
    else:
        punc = ""

    prefixes = ["Blimey! ", "Arrrr! ", "Shiver me timbers! ", "Listen up, ye scurvy dogs: ", "Ayyyy, matey. ",
                "Avast! ", "Well, me hearties, let's see what crawled out of the bung hole. "]
    suffixes = [", me hearties", ", ye scurvy dogs", ", me buxom beauty", ", ye scurvy bilge rats", ", ye scurvy swine",
                ", matey", ", ya horn swogglin' scurvy dog!"]

    rnum = random.randrange(0, 100)
    if 40 < rnum < 70:
        new_chat = random.choice(prefixes) + new_chat
    elif rnum >= 70:
        new_chat += random.choice(suffixes)

    new_chat += punc

    return new_chat


def replace(old_chat):
    replacements = {"hello": "ahoy", "Hello": "Ahoy","hi ": "ahoy ", "Hi ": "Ahoy ",
                    "the ": "th' ", "The ": "Th' ",
                    " to ": " t' ", "To ": "T' ",
                    "woman": "lusty wench", "girl": "lusty wench", "bint": "lusty wench", "bird": "lusty wench",
                    " man": " scurvy landlubber", "boy": "scurvy landlubber", "bloke": "scurvy landlubber",
                    "You ": "Ye ", "you ": "ye ", " you": " ye", "your": "yer", "you're": "yer", "You're": "Yer",
                    "you are": "yer", "You are": "Yer",
                    "kids": "sprogs", "children": "sprogs",
                    "yes ": "aye ", "Yes ": "Aye ",
                    "my ": "me ", "My ": "Me ",
                    "beer": "grog", "Beer": "Grog", "wine": "grog",
                    "fu" + "ck": "roger", "Fu" + "ck": "Roger",
                    "sh" + "it": "sh" + "ite", "Sh" + "it": "Sh" + "ite",
                    " lol": " I be laughin' out loud",
                    "ing ": "in' ", " of ": " a ",
                    " are ": " be ", " is ": " be ",
                    " ones ": " 'uns ", " stop ": " belay ",
                    " and ": " 'n ", " of ": " 'o "}
    new_chat = reduce(lambda x, y: x.replace(y, replacements[y]), replacements, old_chat)

    return new_chat