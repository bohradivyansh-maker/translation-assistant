"""
Example Usage and Testing Script
Demonstrates various features of the Translation Assistant
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.translator import TranslationEngine
from src.context_analyzer import ContextAnalyzer
from src.memory import TranslationMemory
from src.audio_handler import AudioHandler
import logging

logging.basicConfig(level=logging.INFO)


def demo_translation():
    """Demonstrate basic translation"""
    print("\n" + "="*60)
    print("Demo 1: Basic Translation")
    print("="*60)
    
    translator = TranslationEngine()
    
    # Simple translation
    result = translator.translate(
        "Hello, how are you today?",
        target_lang='es'
    )
    
    print(f"\nOriginal:  {result['original_text']}")
    print(f"Translated: {result['translated_text']}")
    print(f"Language:   {result['source_language']} → {result['target_language']}")
    print(f"Confidence: {result['confidence']:.2%}")


def demo_ner():
    """Demonstrate Named Entity Recognition"""
    print("\n" + "="*60)
    print("Demo 2: Named Entity Recognition")
    print("="*60)
    
    analyzer = ContextAnalyzer()
    translator = TranslationEngine()
    
    text = "John Smith works at Microsoft in Seattle on machine learning projects."
    
    # Extract entities
    entities = analyzer.extract_named_entities(text)
    entity_texts = analyzer.get_entity_texts(text)
    
    print(f"\nOriginal text: {text}")
    print(f"\nEntities found:")
    for ent in entities:
        print(f"  - {ent['text']} ({ent['label']})")
    
    # Translate with entity preservation
    result = translator.translate(
        text,
        target_lang='es',
        preserve_entities=entity_texts
    )
    
    print(f"\nTranslation with preserved entities:")
    print(f"  {result['translated_text']}")
    print(f"\nPreserved: {result.get('preserved_entities', [])}")


def demo_context_aware():
    """Demonstrate context-aware translation"""
    print("\n" + "="*60)
    print("Demo 3: Context-Aware Translation")
    print("="*60)
    
    analyzer = ContextAnalyzer()
    translator = TranslationEngine()
    
    full_text = """
    I went to the bank yesterday. It was very crowded.
    I had to wait in line for 30 minutes.
    """
    
    selected = "It was very crowded."
    
    # Extract context
    context = analyzer.extract_context(full_text, selected)
    
    print(f"\nFull text: {full_text.strip()}")
    print(f"\nSelected: {selected}")
    print(f"\nContext before: {context['context_before']}")
    print(f"Context after: {context['context_after']}")
    
    # Translate with context
    result = translator.translate_with_context(
        text=selected,
        context_before=context['context_before'],
        context_after=context['context_after'],
        target_lang='es'
    )
    
    print(f"\nTranslation: {result['translated_text']}")
    print(f"Context used: {result.get('context_used', False)}")


def demo_domain_detection():
    """Demonstrate domain detection"""
    print("\n" + "="*60)
    print("Demo 4: Domain Detection")
    print("="*60)
    
    analyzer = ContextAnalyzer()
    
    texts = {
        "Technical": "The algorithm iterates through the array using a loop to process each element.",
        "Casual": "Hey! How are you doing? Let's hang out later, okay?",
        "Formal": "Pursuant to the aforementioned agreement, we hereby submit this proposal."
    }
    
    for category, text in texts.items():
        analysis = analyzer.analyze_full_context(text)
        
        print(f"\n{category} Text:")
        print(f"  {text[:60]}...")
        print(f"  Detected domain: {analysis['primary_domain']}")
        print(f"  Domain scores: {analysis['domain_scores']}")


def demo_translation_memory():
    """Demonstrate translation memory"""
    print("\n" + "="*60)
    print("Demo 5: Translation Memory")
    print("="*60)
    
    import tempfile
    import os
    
    # Use temporary database
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    memory = TranslationMemory(temp_db.name)
    translator = TranslationEngine()
    
    text = "Good morning"
    
    # First translation (API call)
    print(f"\nFirst translation of: '{text}'")
    result1 = translator.translate(text, target_lang='es')
    
    # Store in memory
    memory.add_translation(
        original_text=text,
        translated_text=result1['translated_text'],
        source_lang=result1['source_language'],
        target_lang=result1['target_language'],
        confidence=result1['confidence']
    )
    print(f"  Translation: {result1['translated_text']}")
    print(f"  Method: {result1['method']}")
    
    # Second translation (from cache)
    print(f"\nSecond translation of: '{text}'")
    cached = memory.find_translation(text, 'en', 'es')
    if cached:
        print(f"  Translation: {cached['translated_text']}")
        print(f"  Method: cache (instant!)")
        print(f"  Usage count: {cached['usage_count']}")
    
    # Statistics
    stats = memory.get_statistics()
    print(f"\nMemory statistics:")
    print(f"  Total translations: {stats['total_translations']}")
    print(f"  Total usage: {stats['total_usage']}")
    
    # Cleanup
    memory.close()
    os.unlink(temp_db.name)


def demo_key_terms():
    """Demonstrate key term extraction"""
    print("\n" + "="*60)
    print("Demo 6: Key Term Extraction (TF-IDF)")
    print("="*60)
    
    analyzer = ContextAnalyzer()
    
    text = """
    Machine learning is a subset of artificial intelligence.
    Deep learning algorithms process data through neural networks.
    The model training requires large datasets and computational resources.
    """
    
    analysis = analyzer.analyze_full_context(text)
    
    print(f"\nText: {text.strip()}")
    print(f"\nKey terms identified:")
    for term, score in analysis['key_terms']:
        print(f"  - {term}: {score:.3f}")
    
    print(f"\nTotal tokens: {analysis['preprocessing']['num_tokens']}")
    print(f"Unique tokens: {analysis['preprocessing']['num_unique_tokens']}")


def demo_audio():
    """Demonstrate text-to-speech"""
    print("\n" + "="*60)
    print("Demo 7: Text-to-Speech")
    print("="*60)
    
    audio = AudioHandler()
    
    texts = [
        ("Hello, this is a test", "en"),
        ("Hola, esto es una prueba", "es"),
        ("Bonjour, ceci est un test", "fr")
    ]
    
    print("\nGenerating audio files...")
    for text, lang in texts:
        filepath = audio.generate_audio(text, lang)
        if filepath:
            print(f"  ✓ Generated: {text[:30]}... ({lang})")
    
    print("\nAudio files generated successfully!")
    print("(In real app, these would be played with button clicks)")


def demo_full_pipeline():
    """Demonstrate complete translation pipeline"""
    print("\n" + "="*60)
    print("Demo 8: Complete Translation Pipeline")
    print("="*60)
    
    translator = TranslationEngine()
    analyzer = ContextAnalyzer()
    
    text = "The algorithm developed by John Smith at MIT shows promising results."
    
    print(f"\nInput: {text}")
    print("\nPipeline steps:")
    
    # Step 1: Analyze
    print("\n1. Analyzing context...")
    analysis = analyzer.analyze_full_context(text)
    print(f"   - Sentences: {len(analysis['sentences'])}")
    print(f"   - Domain: {analysis['primary_domain']}")
    print(f"   - Entities: {len(analysis['entities'])}")
    
    # Step 2: Extract entities
    print("\n2. Extracting named entities...")
    entity_texts = analysis['entity_texts']
    print(f"   - Found: {entity_texts}")
    
    # Step 3: Translate
    print("\n3. Translating...")
    result = translator.translate(
        text,
        target_lang='es',
        preserve_entities=entity_texts
    )
    print(f"   - Result: {result['translated_text']}")
    
    # Step 4: Display metadata
    print("\n4. Translation metadata:")
    print(f"   - Source: {result['source_language']}")
    print(f"   - Target: {result['target_language']}")
    print(f"   - Confidence: {result['confidence']:.2%}")
    print(f"   - Method: {result['method']}")
    print(f"   - Entities preserved: {result.get('preserved_entities', [])}")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("TRANSLATION ASSISTANT - FEATURE DEMONSTRATIONS")
    print("="*60)
    
    demos = [
        demo_translation,
        demo_ner,
        demo_context_aware,
        demo_domain_detection,
        demo_translation_memory,
        demo_key_terms,
        demo_audio,
        demo_full_pipeline
    ]
    
    for demo in demos:
        try:
            demo()
            input("\nPress Enter to continue to next demo...")
        except Exception as e:
            print(f"\n⚠ Demo error: {e}")
            print("Continuing to next demo...")
    
    print("\n" + "="*60)
    print("All demos completed!")
    print("="*60)
    print("\nTo use the full application:")
    print("  python main.py --lang es")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
