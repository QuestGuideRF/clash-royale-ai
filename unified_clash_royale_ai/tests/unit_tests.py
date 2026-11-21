import unittest
import numpy as np
import sys
import os
sys .path .insert (0 ,os .path .dirname (os .path .dirname (os .path .dirname (__file__ ))))
class TestCardsDatabase (unittest .TestCase ):
    def test_get_card_info (self ):
        from unified_clash_royale_ai .data .cards_database import get_card_info
        info =get_card_info ('knight')
        self .assertIsNotNone (info )
        self .assertIn ('elixir',info )
        self .assertEqual (info ['elixir'],3 )
    def test_get_card_info_invalid (self ):
        from unified_clash_royale_ai .data .cards_database import get_card_info
        info =get_card_info ('invalid_card_name')
        self .assertIsNone (info )
    def test_get_all_cards (self ):
        from unified_clash_royale_ai .data .cards_database import get_all_cards
        cards =get_all_cards ()
        self .assertIsInstance (cards ,dict )
        self .assertGreater (len (cards ),0 )
class TestElixirTracker (unittest .TestCase ):
    def setUp (self ):
        from unified_clash_royale_ai .strategies .advanced .elixir_tracker import ElixirTracker
        self .tracker =ElixirTracker ()
    def test_initial_elixir (self ):
        self .assertEqual (self .tracker .get_our_elixir (),5 )
    def test_record_card (self ):
        initial =self .tracker .get_our_elixir ()
        self .tracker .record_our_card ('knight')
        self .assertEqual (self .tracker .get_our_elixir (),initial -3 )
    def test_cant_go_negative (self ):
        for _ in range (5 ):
            self .tracker .record_our_card ('golem')
        self .assertGreaterEqual (self .tracker .get_our_elixir (),0 )
class TestCycleCounter (unittest .TestCase ):
    def setUp (self ):
        from unified_clash_royale_ai .strategies .advanced .cycle_counter import CycleCounter
        self .counter =CycleCounter ()
        self .test_deck =['knight','archers','fireball','zap',
        'hog_rider','musketeer','ice_golem','cannon']
        self .counter .set_our_deck (self .test_deck )
    def test_initial_hand (self ):
        hand =self .counter .get_our_hand ()
        self .assertEqual (len (hand ),4 )
        self .assertEqual (hand ,self .test_deck [:4 ])
    def test_play_card (self ):
        self .counter .record_our_play ('knight')
        hand =self .counter .get_our_hand ()
        self .assertNotIn ('knight',hand )
        self .assertEqual (len (hand ),4 )
    def test_next_card (self ):
        next_card =self .counter .get_our_next_card ()
        self .assertEqual (next_card ,'hog_rider')
class TestDeckBuilder (unittest .TestCase ):
    def setUp (self ):
        from unified_clash_royale_ai .strategies .advanced .deck_builder import DeckBuilder
        self .builder =DeckBuilder ()
    def test_build_deck (self ):
        deck =self .builder .build_deck ('beatdown')
        self .assertIn ('cards',deck )
        self .assertEqual (len (deck ['cards']),8 )
    def test_get_popular_decks (self ):
        decks =self .builder .get_popular_decks ()
        self .assertIsInstance (decks ,list )
        self .assertGreater (len (decks ),0 )
class TestCacheManager (unittest .TestCase ):
    def setUp (self ):
        from unified_clash_royale_ai .performance .cache_manager import CacheManager
        self .cache =CacheManager (max_size =10 ,ttl =5 )
    def test_set_get (self ):
        self .cache .set ('key1','value1')
        self .assertEqual (self .cache .get ('key1'),'value1')
    def test_get_nonexistent (self ):
        self .assertIsNone (self .cache .get ('nonexistent'))
    def test_lru_eviction (self ):
        for i in range (15 ):
            self .cache .set (f'key{i }',f'value{i }')
        self .assertIsNone (self .cache .get ('key0'))
    def test_stats (self ):
        self .cache .set ('key1','value1')
        self .cache .get ('key1')
        self .cache .get ('key2')
        stats =self .cache .get_stats ()
        self .assertEqual (stats ['hits'],1 )
        self .assertEqual (stats ['misses'],1 )
class TestMatchupAnalyzer (unittest .TestCase ):
    def setUp (self ):
        from unified_clash_royale_ai .strategies .advanced .matchup_analyzer import MatchupAnalyzer
        self .analyzer =MatchupAnalyzer ()
    def test_analyze_matchup (self ):
        our_deck =['hog_rider','musketeer','fireball','zap',
        'knight','archers','cannon','ice_golem']
        opponent_deck =['golem','night_witch','baby_dragon','mega_minion',
        'lightning','tornado','tombstone','lumberjack']
        analysis =self .analyzer .analyze_matchup (our_deck ,opponent_deck )
        self .assertIn ('advantage_score',analysis )
        self .assertIn ('strategy_tips',analysis )
    def test_get_matchup_rating (self ):
        our_deck =['knight']*8
        opponent_deck =['knight']*8
        rating =self .analyzer .get_matchup_rating (our_deck ,opponent_deck )
        self .assertGreaterEqual (rating ,0 )
        self .assertLessEqual (rating ,100 )
if __name__ =='__main__':
    unittest .main ()