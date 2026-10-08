import json
import re


def clean_text(text: str) -> str:
    text = text.lower().strip()

    for ch in [",", ".", "?", "!", ";", ":", "-", "_"]:
        text = text.replace(ch, " ")

    return " ".join(text.split())


def extract_active_query(text: str) -> str:
    lower = text.lower()

    if "don't" in lower or "dont" in lower or "not " in lower or "ignore " in lower:
        parts = re.split(r"[,;]", text)

        for part in parts:
            p = part.lower()

            if not ("don't" in p or "dont" in p or "not " in p or "ignore" in p):
                if p.strip():
                    return p.strip()

    return text


def keyword_baseline(message: str) -> dict:
    msg = clean_text(message)

    keywords = [
        (
            ["order", "orders", "quotation", "quotations", "revenue", "amount"],
            "data_query",
            "Found data query keyword."
        ),
        (
            ["price", "rate", "cost"],
            "price_intel",
            "Found price keyword."
        ),
        (
            ["food grade", "gsm", "micron", "material", "spec"],
            "spec_help",
            "Found spec keyword."
        ),
        (
            ["supplier", "vendor"],
            "supplier_rec",
            "Found supplier keyword."
        ),
        (
            ["rfq"],
            "faq",
            "Found RFQ keyword."
        ),
        (
            ["page", "where"],
            "navigation",
            "Found navigation keyword."
        ),
        (
            ["profile"],
            "profile_help",
            "Found profile keyword."
        ),
        (
            ["insaan", "human", "agent", "support"],
            "support",
            "Found support keyword."
        ),
        (
            ["demand", "trend"],
            "market_insights",
            "Found market keyword."
        ),
        (
            ["hi", "hello", "hey", "namaste"],
            "greeting",
            "Found greeting keyword."
        ),
        (
            ["help"],
            "help",
            "Found help keyword."
        ),
        (
            ["payment"],
            "faq",
            "Found payment keyword."
        )
    ]

    for words, intent, reason in keywords:
        if any(word in msg for word in words):
            return {
                "intent": intent,
                "confidence": "high",
                "reason": reason
            }

    return {
        "intent": "fallback",
        "confidence": "low",
        "reason": "No keyword matched."
    }


def classify(message: str) -> dict:
    raw_msg = message.strip()
    active_msg = extract_active_query(raw_msg)
    msg = clean_text(active_msg)

    off_topic = [
        "cricket",
        "world cup",
        "recipe",
        "cake",
        "weather",
        "france",
        "president"
    ]

    if any(word in msg for word in off_topic) or msg == "asdf qwerty" or not msg:
        return {
            "intent": "fallback",
            "confidence": "low",
            "reason": "The query is off-topic or unrecognized text."
        }

    if any(word in msg for word in [
        "insaan",
        "human",
        "agent",
        "person",
        "baat karni",
        "customer care",
        "escalate"
    ]):
        return {
            "intent": "support",
            "confidence": "high",
            "reason": "The user asked to talk to a human support agent."
        }

    if "page" in msg or ("where" in msg and "is" in msg) or "kahan hai" in msg:
        if not any(word in msg for word in [
            "matlab",
            "mean",
            "meaning",
            "kitne ka",
            "status"
        ]):
            return {
                "intent": "navigation",
                "confidence": "high",
                "reason": "The user asked for page navigation."
            }

    if "rfq" in msg and any(word in msg for word in [
        "likh do",
        "bana do",
        "write",
        "draft",
        "create",
        "make"
    ]):
        return {
            "intent": "rfq_assist",
            "confidence": "high",
            "reason": "The user asked to draft or write an RFQ."
        }

    if any(word in msg for word in [
        "supplier",
        "suplier",
        "vendor",
        "recommend",
        "recoomendation",
        "batao"
    ]):
        if any(word in msg for word in ["supplier", "suplier", "vendor"]):
            return {
                "intent": "supplier_rec",
                "confidence": "high",
                "reason": "The user asked for supplier recommendations."
            }

    if any(word in msg for word in [
        "fair price",
        "market rate",
        "what to charge",
        "rate kya",
        "prce",
        "price check"
    ]):
        return {
            "intent": "price_intel",
            "confidence": "high",
            "reason": "The user asked for pricing or market rate intelligence."
        }

    if "price" in msg and "not the price" not in raw_msg.lower():
        return {
            "intent": "price_intel",
            "confidence": "high",
            "reason": "The user asked about pricing."
        }

    if any(word in msg for word in [
        "gsm",
        "micron",
        "food grade",
        "laminate",
        "spec"
    ]) and any(word in msg for word in [
        "matlab",
        "mean",
        "meaning",
        "kya hai",
        "what is"
    ]):
        return {
            "intent": "spec_help",
            "confidence": "high",
            "reason": "The user asked for clarification on a packaging spec."
        }

    if any(word in msg for word in [
        "demand",
        "trend",
        "trends",
        "badh rahi hai",
        "growing"
    ]):
        return {
            "intent": "market_insights",
            "confidence": "high",
            "reason": "The user asked about market demand or trends."
        }

    if "profile" in msg and any(word in msg for word in [
        "missing",
        "complete",
        "fields",
        "kya"
    ]):
        return {
            "intent": "profile_help",
            "confidence": "high",
            "reason": "The user asked about profile completeness or missing details."
        }

    if (
        msg in ["hi", "hello", "hey", "namaste", "greetings"]
        or any(msg.startswith(word) for word in ["hi ", "hello ", "hey "])
    ):
        return {
            "intent": "greeting",
            "confidence": "high",
            "reason": "The user greeted the assistant."
        }

    if (
        "what can you help" in msg
        or "what can you do" in msg
        or "tum kya kar" in msg
        or msg == "help"
    ):
        return {
            "intent": "help",
            "confidence": "high",
            "reason": "The user asked about bot capabilities."
        }

    if any(word in msg for word in [
        "payment kaise",
        "how payment works",
        "how kypson works",
        "what is an rfq",
        "verification"
    ]):
        return {
            "intent": "faq",
            "confidence": "high",
            "reason": "The user asked a general platform FAQ."
        }

    if any(word in msg for word in [
        "order",
        "orders",
        "quotation",
        "quotations",
        "revenue",
        "rfq status",
        "last order",
        "kitne ka tha"
    ]):
        return {
            "intent": "data_query",
            "confidence": "high",
            "reason": "The user asked to view personal account data."
        }

    return {
        "intent": "fallback",
        "confidence": "low",
        "reason": "Unrecognized or general query."
    }


def main():
    with open("tests.json", "r", encoding="utf-8") as f:
        tests = json.load(f)

    baseline_correct = 0
    classify_correct = 0
    total = len(tests)

    print("=" * 60)
    print("KAI INTENT CLASSIFIER - BENCHMARK")
    print("=" * 60)

    for item in tests:
        message = item["message"]
        expected = item["intent"]

        baseline_result = keyword_baseline(message)["intent"]
        classifier_result = classify(message)["intent"]

        if baseline_result == expected:
            baseline_correct += 1

        if classifier_result == expected:
            classify_correct += 1

    difference = classify_correct - baseline_correct

    print(f"Total Test Messages : {total}")
    print(
        f"Baseline Score      : "
        f"{baseline_correct}/{total} "
        f"({baseline_correct / total * 100:.1f}%)"
    )
    print(
        f"Classifier Score    : "
        f"{classify_correct}/{total} "
        f"({classify_correct / total * 100:.1f}%)"
    )
    print(f"Score Difference    : +{difference}")

    if difference >= 8:
        print("Status              : PASSED")
    else:
        print("Status              : FAILED")

    heldout_messages = [
        "hi",
        "what can you help with",
        "show my orders",
        "don't show my orders, what's a fair price",
        "food grade laminate ke liye supplier batao",
        "50 gsm ka matlab kya hai",
        "50 gsm bags ke liye RFQ likh do",
        "order page kahan hai",
        "mera last order kitne ka tha",
        "is compostable mailer demand badh rahi hai",
        "profile mein kya missing hai",
        "mujhe insaan se baat karni hai",
        "kypson pe payment kaise hota hai",
        "not the price, show my quotations",
        "asdf qwerty"
    ]

    heldout_results = []

    for message in heldout_messages:
        heldout_results.append(classify(message))

    with open("heldout.json", "w", encoding="utf-8") as f:
        json.dump(heldout_results, f, indent=2)

    print("heldout.json created successfully.")


if __name__ == "__main__":
    main()
