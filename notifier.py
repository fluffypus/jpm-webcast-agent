def notify(result):
    print("\n🚨 WEBCAST SIGNAL DÉTECTÉ")
    print(f"Company   : {result['company']}")
    print(f"Session   : {result['session']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Score     : {result['score']}")
    if result["links"]:
        print("Links:")
        for l in result["links"]:
            print(f"  - {l}")
