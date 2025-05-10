import csv
import os
import time
from datetime import datetime


class GameStats:
    def __init__(self):
        self.stats_file = "game_stats.csv"
        self.ensure_stats_file_exists()

        # Initialize counters for the current game
        self.reset_current_game_stats()

    def reset_current_game_stats(self):
        """Reset all stats for a new game"""
        self.battle_count = 0
        self.soldiers_created = 0
        self.farmers_created = 0
        self.hearts_lost_player1 = 0
        self.hearts_lost_player2 = 0
        self.game_start_time = time.time()
        self.turn_count = 0
        self.action_types = {"attack": 0, "heal": 0, "damage": 0, "play_card": 0}

    def ensure_stats_file_exists(self):
        """Create the stats CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Date", "Player1", "Player2", "Winner",
                    "BattleCount", "SoldiersCreated", "FarmersCreated",
                    "HeartsLostPlayer1", "HeartsLostPlayer2",
                    "GameDuration", "TurnCount", "AttackActions",
                    "HealActions", "DamageBoostActions", "CardActions"
                ])

    def record_battle(self):
        """Increment battle counter"""
        self.battle_count += 1

    def record_unit_allocation(self, soldiers, farmers):
        """Record unit allocation"""
        self.soldiers_created += soldiers
        self.farmers_created += farmers

    def record_hearts_lost(self, player, amount):
        """Record hearts lost by a player"""
        if player == "player1":
            self.hearts_lost_player1 += amount
        else:
            self.hearts_lost_player2 += amount

    def record_action(self, action_type):
        """Record an action type"""
        if action_type in self.action_types:
            self.action_types[action_type] += 1

    def increment_turn(self):
        """Increment turn counter"""
        self.turn_count += 1

    def save_game_stats(self, player1_name, player2_name, winner_name):
        """Save all stats for the current game to CSV"""
        game_duration = time.time() - self.game_start_time

        with open(self.stats_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                player1_name,
                player2_name,
                winner_name,
                self.battle_count,
                self.soldiers_created,
                self.farmers_created,
                self.hearts_lost_player1,
                self.hearts_lost_player2,
                round(game_duration, 2),
                self.turn_count,
                self.action_types["attack"],
                self.action_types["heal"],
                self.action_types["damage"],
                self.action_types["play_card"]
            ])