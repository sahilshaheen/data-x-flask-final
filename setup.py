import sqlite3

seed_values = [("""Director Michel Gondry, whose specialty in music videos was a seamless visual blending of reality and surreality, was the perfect filmmaker for this thoughtful, provoking drama which juggles past and present. Jim Carrey is excellent as a single man looking for love...and perhaps finding it with eccentric clerk Kate Winslet; unfortunately, a double-header secret from both their pasts may come back to haunt them. Gondry, who also worked on the original story with Pierre Bismuth and screenwriter Charlie Kaufman, is masterful with a flashy scenario (both figuratively and literally), and he works surprisingly well with his eclectic group of actors. However, the characters in Kaufman's script aren't especially likable (particularly Winslet's argumentative love-interest) and the film is acutely chilly, with everybody bundled up and shivering. As the plot thickens, it also becomes convoluted (and, purposely one assumes, splintered); despite some missteps, Gondry works nimbly steering the viewer through the mechanisms of the narrative, and there several engaging or arresting sequences. Similar in tone and spirit to "Being John Malkovich", which Kaufman also wrote, and blazing with deft, daring originality.""", "positive", "correct"),
        ("""The story gets increasingly more bizarre. There are no explanations or closures either. I honestly don't know what I watched.""", "positive", "wrong"),
        ("""Random things happening with random chronology. Question everything you see and make out whatever interpretations you want. If you like stuff like that, you'll probably love this. For me? I'm so fed up with movies like this, it just became so lame to make movies like this with being confusing for the sake of being confusing and forcing us making it out with interpretations.""", "negative", "correct")]


def create_schema(seed):
    conn = sqlite3.connect('predictions.db')

    conn.execute("DROP TABLE IF EXISTS results")

    conn.execute("""
    CREATE TABLE results (
        id INTEGER PRIMARY KEY,
        review TEXT NOT NULL,
        prediction TEXT NOT NULL,
        feedback TEXT
    );
    """)

    print("CREATED results")

    if seed:
        cur = conn.cursor()
        for i in seed_values:
            cur.execute("""
            INSERT INTO results (review, prediction, feedback)
            VALUES (?, ?, ?);
            """, i)
        conn.commit()
        print("Added seed values")

    conn.close()

    print("Connection closed")


if __name__ == "__main__":
    create_schema()
