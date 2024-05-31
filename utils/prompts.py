class FactPrompts():
    general_facts_english="""{{
    "prompt": "Generate a short, suspenseful, and engaging fact about {topic} suitable for a YouTube short. The fact should be concise, structured in two parts: the first part to build suspense and intrigue, prompting curiosity, and the second part to provide a surprising or insightful reveal in a few words. Also give the description of the image releavant to the topic. Aim for brevity and captivation to encourage viewers to watch until the end.",
    "response_format": "json",
    "example": {{
    "Output": {{
        "Part_1": "In the depths of the jungle, a mysterious predator lurks unseen...",
        "Part_2": "Only its amber eyes reveal the presence of the elusive tiger."
    }},
    "image_description": "An image of a majestic tiger camouflaged among lush green foliage in the jungle, with its piercing amber eyes staring directly at the viewer, conveying a sense of primal power and hidden danger."
    }}
    }}"""
