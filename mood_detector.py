from textblob import TextBlob
import re

MOOD_KEYWORDS = {
    "happy": ["happy", "joyful", "great", "amazing", "wonderful", "fantastic", "cheerful", "excited", "elated", "blessed"],
    "sad": ["sad", "unhappy", "down", "blue", "depressed", "miserable", "upset", "crying", "tears", "heartache"],
    "heartbroken": ["heartbroken", "broken", "devastated", "crushed", "shattered", "betrayed", "dumped", "lost them", "miss them"],
    "romantic": ["romantic", "love", "in love", "affection", "intimate", "adore", "devoted", "soulmate", "together"],
    "flirty": ["flirty", "crush", "flirt", "butterflies", "attracted", "seductive", "charming", "playful love"],
    "nostalgic": ["nostalgic", "memories", "remember", "past", "childhood", "throwback", "miss the old", "back then"],
    "dreamy": ["dreamy", "dreaming", "fantasy", "floating", "surreal", "lost in thought", "daydream", "hazy"],
    "chill": ["chill", "relaxed", "laid back", "easygoing", "vibing", "mellow", "no stress", "lofi"],
    "peaceful": ["peaceful", "serene", "tranquil", "calm", "quiet", "still", "at peace", "zen", "meditate"],
    "emotional": ["emotional", "feeling a lot", "overwhelmed", "deep feelings", "moved", "touched", "teary"],
    "bittersweet": ["bittersweet", "happy but sad", "mixed feelings", "complicated", "bitter", "sweet and sad"],
    "hopeful": ["hopeful", "hope", "looking forward", "better days", "optimistic", "things will get better"],
    "healing": ["healing", "recovering", "getting better", "moving on", "self care", "therapy", "growing"],
    "motivational": ["motivated", "motivation", "grind", "hustle", "push through", "keep going", "never give up"],
    "confident": ["confident", "confidence", "self assured", "believe in myself", "unstoppable", "i got this"],
    "powerful": ["powerful", "power", "strong", "strength", "force", "dominant", "bold", "fierce"],
    "hype": ["hype", "hyped", "pumped", "amped", "lit", "fire", "turnt", "going off", "energy"],
    "party": ["party", "celebrate", "dancing", "club", "night out", "drinks", "fun night", "banger"],
    "energetic": ["energetic", "energy", "active", "workout", "gym", "run", "intense", "fired up"],
    "aggressive": ["aggressive", "rage", "furious", "violent", "intense anger", "fed up", "explode"],
    "angry": ["angry", "mad", "frustrated", "annoyed", "irritated", "pissed", "hate", "upset"],
    "dark": ["dark", "darkness", "sinister", "gloomy", "doom", "heavy", "black", "shadow", "evil"],
    "mysterious": ["mysterious", "mystery", "enigmatic", "unknown", "cryptic", "eerie", "strange", "mystical"],
    "cinematic": ["cinematic", "epic scene", "movie moment", "dramatic", "film", "score", "soundtrack"],
    "ethereal": ["ethereal", "celestial", "cosmic", "otherworldly", "angelic", "spiritual", "divine", "heavenly"],
    "playful": ["playful", "silly", "goofy", "fun", "games", "jokes", "lighthearted", "bubbly"],
    "epic": ["epic", "legendary", "massive", "grand", "huge", "monumental", "glorious", "heroic"],
    "soulful": ["soulful", "soul", "deep", "heartfelt", "raw emotion", "blues", "gospel", "genuine"],
    "introspective": ["introspective", "thinking", "reflect", "soul searching", "deep thought", "self aware"],
    "lonely": ["lonely", "alone", "isolated", "no one", "abandoned", "forgotten", "by myself", "solitude"],
    "vulnerable": ["vulnerable", "exposed", "fragile", "open", "raw", "soft", "scared to feel", "defenseless"],
    "yearning": ["yearning", "longing", "missing", "wish you were here", "want you back", "aching for"],
    "melancholic": ["melancholic", "melancholy", "gloomy", "somber", "wistful", "sorrowful", "heavy heart"],
    "rebellious": ["rebellious", "rebel", "against the rules", "dont care", "break free", "anarchy", "defiant"],
    "fearless": ["fearless", "brave", "courageous", "no fear", "bold", "daring", "unstoppable", "face it"],
    "sensual": ["sensual", "sexy", "seductive", "intimate", "desire", "passionate", "steamy", "alluring"],
    "cozy": ["cozy", "comfy", "warm blanket", "home", "snug", "couch", "hot chocolate", "fireplace"],
    "warm": ["warm", "warmth", "golden", "sunshine", "soft glow", "gentle", "loving feeling"],
    "summer": ["summer", "beach", "sun", "ocean", "hot day", "summer vibes", "vacation", "holiday"],
    "late_night": ["late night", "midnight", "3am", "cant sleep", "night drive", "city lights", "insomnia"],
    "roadtrip": ["road trip", "driving", "highway", "open road", "windows down", "adventure drive"],
    "rainy_day": ["rainy", "rain", "rainy day", "storm", "thunder", "cloudy", "grey sky", "drizzle"],
    "main_character": ["main character", "protagonist", "my moment", "like a movie", "walking into", "cinematic life"],
    "chaotic": ["chaotic", "chaos", "crazy", "unhinged", "wild", "out of control", "madness", "insane"],
    "soft_acoustic": ["acoustic", "soft", "unplugged", "guitar", "simple", "stripped", "raw acoustic"],
    "indie": ["indie", "alternative", "indie pop", "indie rock", "underground", "lo-fi indie", "bedroom pop"],
    "retro": ["retro", "vintage", "old school", "classic", "throwback", "80s", "90s", "70s", "nostalgia"],
    "fantasy": ["fantasy", "magical", "enchanted", "wizard", "fairy tale", "mythical", "dragon", "elf"],
    "adventurous": ["adventure", "adventurous", "explore", "journey", "discover", "quest", "thrill", "brave"],
    "triumphant": ["triumphant", "victory", "won", "champion", "conquered", "achieved", "overcame", "success"],
}

MOOD_PROFILES = {
    "happy":          {"valence": 0.90, "energy": 0.80, "danceability": 0.85},
    "sad":            {"valence": 0.20, "energy": 0.25, "danceability": 0.30},
    "heartbroken":    {"valence": 0.15, "energy": 0.20, "danceability": 0.25},
    "romantic":       {"valence": 0.75, "energy": 0.45, "danceability": 0.55},
    "flirty":         {"valence": 0.80, "energy": 0.65, "danceability": 0.75},
    "nostalgic":      {"valence": 0.55, "energy": 0.35, "danceability": 0.45},
    "dreamy":         {"valence": 0.70, "energy": 0.35, "danceability": 0.45},
    "chill":          {"valence": 0.60, "energy": 0.30, "danceability": 0.50},
    "peaceful":       {"valence": 0.65, "energy": 0.20, "danceability": 0.30},
    "emotional":      {"valence": 0.35, "energy": 0.40, "danceability": 0.35},
    "bittersweet":    {"valence": 0.45, "energy": 0.35, "danceability": 0.40},
    "hopeful":        {"valence": 0.75, "energy": 0.60, "danceability": 0.60},
    "healing":        {"valence": 0.65, "energy": 0.40, "danceability": 0.45},
    "motivational":   {"valence": 0.80, "energy": 0.85, "danceability": 0.75},
    "confident":      {"valence": 0.80, "energy": 0.75, "danceability": 0.70},
    "powerful":       {"valence": 0.75, "energy": 0.90, "danceability": 0.70},
    "hype":           {"valence": 0.85, "energy": 0.95, "danceability": 0.90},
    "party":          {"valence": 0.90, "energy": 0.90, "danceability": 0.95},
    "energetic":      {"valence": 0.75, "energy": 0.95, "danceability": 0.85},
    "aggressive":     {"valence": 0.20, "energy": 0.95, "danceability": 0.50},
    "angry":          {"valence": 0.20, "energy": 0.90, "danceability": 0.45},
    "dark":           {"valence": 0.15, "energy": 0.70, "danceability": 0.40},
    "mysterious":     {"valence": 0.40, "energy": 0.50, "danceability": 0.45},
    "cinematic":      {"valence": 0.55, "energy": 0.65, "danceability": 0.40},
    "ethereal":       {"valence": 0.65, "energy": 0.40, "danceability": 0.35},
    "playful":        {"valence": 0.85, "energy": 0.70, "danceability": 0.85},
    "epic":           {"valence": 0.70, "energy": 0.90, "danceability": 0.60},
    "soulful":        {"valence": 0.60, "energy": 0.50, "danceability": 0.55},
    "introspective":  {"valence": 0.40, "energy": 0.30, "danceability": 0.35},
    "lonely":         {"valence": 0.20, "energy": 0.20, "danceability": 0.25},
    "vulnerable":     {"valence": 0.30, "energy": 0.25, "danceability": 0.30},
    "yearning":       {"valence": 0.35, "energy": 0.30, "danceability": 0.35},
    "melancholic":    {"valence": 0.25, "energy": 0.25, "danceability": 0.30},
    "rebellious":     {"valence": 0.50, "energy": 0.85, "danceability": 0.65},
    "fearless":       {"valence": 0.80, "energy": 0.85, "danceability": 0.70},
    "sensual":        {"valence": 0.70, "energy": 0.60, "danceability": 0.75},
    "cozy":           {"valence": 0.70, "energy": 0.25, "danceability": 0.40},
    "warm":           {"valence": 0.75, "energy": 0.40, "danceability": 0.50},
    "summer":         {"valence": 0.85, "energy": 0.80, "danceability": 0.85},
    "late_night":     {"valence": 0.45, "energy": 0.55, "danceability": 0.60},
    "roadtrip":       {"valence": 0.80, "energy": 0.75, "danceability": 0.70},
    "rainy_day":      {"valence": 0.35, "energy": 0.25, "danceability": 0.30},
    "main_character": {"valence": 0.80, "energy": 0.75, "danceability": 0.70},
    "chaotic":        {"valence": 0.50, "energy": 0.95, "danceability": 0.65},
    "soft_acoustic":  {"valence": 0.60, "energy": 0.25, "danceability": 0.40},
    "indie":          {"valence": 0.55, "energy": 0.50, "danceability": 0.55},
    "retro":          {"valence": 0.70, "energy": 0.65, "danceability": 0.70},
    "fantasy":        {"valence": 0.65, "energy": 0.55, "danceability": 0.45},
    "adventurous":    {"valence": 0.75, "energy": 0.80, "danceability": 0.65},
    "triumphant":     {"valence": 0.85, "energy": 0.90, "danceability": 0.75},
}


def detect_mood(text: str) -> dict:
    text_lower = re.sub(r'[^\w\s]', ' ', text.lower())
    best_mood = None
    best_score = 0
    for mood, keywords in MOOD_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > best_score:
            best_score = score
            best_mood = mood
    if best_mood and best_score > 0:
        profile = MOOD_PROFILES.get(best_mood, {"valence": 0.5, "energy": 0.5, "danceability": 0.5})
        return {"label": best_mood, **profile}
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    valence = (polarity + 1) / 2
    energy = 0.4 + (subjectivity * 0.4)
    danceability = (valence + energy) / 2
    if polarity > 0.3:
        label = "happy"
    elif polarity < -0.3:
        label = "sad"
    elif energy > 0.6:
        label = "energetic"
    else:
        label = "chill"
    return {"label": label, "valence": round(valence, 2), "energy": round(energy, 2), "danceability": round(danceability, 2)}
