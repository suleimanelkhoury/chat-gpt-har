from scholarly import scholarly
# Prompts
def get_functions():
    return {
        "Function 1": {
            # Preface
            "Prefix":   r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, " +
                        r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. " +
                        r"Furthermore, list all modification and explain the reasons to do so in markdown table." + "\n\n",
            # Postscript
            "Suffix":   r"",
            "Color":    r"secondary",    # button color
        },
        "Find Related Works": {
            # Preface
            "Prefix":   r"You are a research assistant and tasked with finding all the relevant research papers that were cited by " +
                        r"a certain paper. Now you still need the name of said paper. For tell the user <Please provide me with the " + 
                        r"name of the paper in question.> Then the user will give you the name of the paper. Your next message should " + 
                        r"then be a list of the top 10 papers that have cited the paper provided to you by the user." + "\n\n",
            # Postscript
            "Suffix":   r"",
            "Color":    r"secondary",    # button color
        },
        "Function 3": {
            # Preface
            "Prefix":   r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, " +
                        r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. " +
                        r"Furthermore, list all modification and explain the reasons to do so in markdown table." + "\n\n",
            # Postscript
            "Suffix":   r"",
            "Color":    r"secondary",    # button color
        },
        "Function 4": {
            # Preface
            "Prefix":   r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, " +
                        r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. " +
                        r"Furthermore, list all modification and explain the reasons to do so in markdown table." + "\n\n",
            # Postscript
            "Suffix":   r"",
            "Color":    r"secondary",    # button color
        },
    }

