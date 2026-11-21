import unittest
import numpy as np
import sys
import os
import tempfile
import shutil
sys .path .insert (0 ,os .path .dirname (os .path .dirname (os .path .dirname (__file__ ))))
class TestBotIntegration (unittest .TestCase ):
    @classmethod
    def setUpClass (cls ):
        cls .temp_dir =tempfile .mkdtemp ()
    @classmethod
    def tearDownClass (cls ):
        shutil .rmtree (cls .temp_dir ,ignore_errors =True )
    def test_game_state_creation (self ):
        from unified_clash_royale_ai .game_automation .game_state import GameState
        state =GameState ()
        self .assertIsNotNone (state )
        self .assertEqual (state .our_elixir ,5 )
    def test_game_state_update (self ):
        from unified_clash_royale_ai .game_automation .game_state import GameState
        state =GameState ()
        test_frame =np .zeros ((1024 ,600 ,3 ),dtype =np .uint8 )
        try :
            state .update (test_frame )
            success =True
        except Exception as e :
            success =False
        self .assertTrue (success )
class TestTrainingIntegration (unittest .TestCase ):
    @classmethod
    def setUpClass (cls ):
        cls .temp_dir =tempfile .mkdtemp ()
    @classmethod
    def tearDownClass (cls ):
        shutil .rmtree (cls .temp_dir ,ignore_errors =True )
    def test_model_manager (self ):
        from unified_clash_royale_ai .training .model_manager import ModelManager
        manager =ModelManager (
        models_dir =os .path .join (self .temp_dir ,'models'),
        cache_dir =os .path .join (self .temp_dir ,'cache')
        )
        self .assertIsNotNone (manager )
        self .assertEqual (manager .versions ,{})
    def test_data_collector (self ):
        from unified_clash_royale_ai .training .data_collection import DataCollector
        collector =DataCollector (output_dir =os .path .join (self .temp_dir ,'data'))
        stats =collector .get_statistics ()
        self .assertIn ('cards',stats )
        self .assertIn ('yolo',stats )
class TestReplayIntegration (unittest .TestCase ):
    @classmethod
    def setUpClass (cls ):
        cls .temp_dir =tempfile .mkdtemp ()
        cls .test_replay_dir =os .path .join (cls .temp_dir ,'recordings','test_match')
        os .makedirs (cls .test_replay_dir ,exist_ok =True )
        import json
        with open (os .path .join (cls .test_replay_dir ,'metadata.json'),'w')as f :
            json .dump ({
            'result':'win',
            'recorded_at':'2024-01-01T00:00:00',
            'total_frames':100
            },f )
        with open (os .path .join (cls .test_replay_dir ,'actions.json'),'w')as f :
            json .dump ([
            {'frame_id':10 ,'action':{'card':'knight'}},
            {'frame_id':50 ,'action':{'card':'fireball'}}
            ],f )
    @classmethod
    def tearDownClass (cls ):
        shutil .rmtree (cls .temp_dir ,ignore_errors =True )
    def test_replay_parser (self ):
        from unified_clash_royale_ai .replay_analyzer .replay_parser import ReplayParser
        parser =ReplayParser (recordings_dir =os .path .join (self .temp_dir ,'recordings'))
        replays =parser .list_replays ()
        self .assertEqual (len (replays ),1 )
        replay =parser .load_replay ('test_match')
        self .assertEqual (replay .result ,'win')
    def test_improvement_advisor (self ):
        from unified_clash_royale_ai .replay_analyzer .replay_parser import ReplayParser
        from unified_clash_royale_ai .replay_analyzer .improvement_advisor import ImprovementAdvisor
        parser =ReplayParser (recordings_dir =os .path .join (self .temp_dir ,'recordings'))
        replay =parser .load_replay ('test_match')
        advisor =ImprovementAdvisor ()
        analysis =advisor .analyze_and_advise (replay )
        self .assertIn ('recommendations',analysis )
        self .assertIn ('overall_score',analysis )
class TestStrategyIntegration (unittest .TestCase ):
    def test_full_strategy_pipeline (self ):
        from unified_clash_royale_ai .strategies .advanced .elixir_tracker import ElixirTracker
        from unified_clash_royale_ai .strategies .advanced .cycle_counter import CycleCounter
        from unified_clash_royale_ai .strategies .advanced .matchup_analyzer import MatchupAnalyzer
        elixir =ElixirTracker ()
        cycle =CycleCounter ()
        matchup =MatchupAnalyzer ()
        our_deck =['hog_rider','musketeer','fireball','zap',
        'knight','archers','cannon','ice_golem']
        cycle .set_our_deck (our_deck )
        elixir .record_our_card ('knight')
        cycle .record_our_play ('knight')
        self .assertEqual (elixir .get_our_elixir (),2 )
        self .assertNotIn ('knight',cycle .get_our_hand ())
        elixir .record_opponent_card ('golem')
        cycle .record_opponent_play ('golem')
        opponent_deck =cycle .get_opponent_seen_cards ()+['unknown']*7
        self .assertIn ('golem',cycle .get_opponent_seen_cards ())
class TestPerformanceIntegration (unittest .TestCase ):
    def test_cache_with_processing (self ):
        from unified_clash_royale_ai .performance .cache_manager import CacheManager
        from unified_clash_royale_ai .performance .frame_processor import FrameProcessor
        cache =CacheManager (max_size =10 )
        processor =FrameProcessor (num_workers =2 )
        test_frame =np .random .randint (0 ,255 ,(480 ,640 ,3 ),dtype =np .uint8 )
        cache .set ('test_frame',test_frame )
        cached =cache .get ('test_frame')
        self .assertIsNotNone (cached )
        np .testing .assert_array_equal (test_frame ,cached )
if __name__ =='__main__':
    unittest .main ()