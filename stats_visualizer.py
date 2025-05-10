"""
Castle War Game - Statistics Visualizer
This script analyzes game_stats.csv and creates various visualizations
to help understand player behavior and game balance.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class GameStatsVisualizer:
    def __init__(self, stats_file="game_stats.csv"):
        self.stats_file = stats_file
        self.df = None
        self.load_data()
        # Set a consistent style for all plots
        plt.style.use('ggplot')
        sns.set_palette("Set2")

    def load_data(self):
        """Load data from CSV file"""
        if not os.path.exists(self.stats_file):
            print(f"Error: {self.stats_file} not found!")
            return False

        try:
            self.df = pd.read_csv(self.stats_file)
            # Convert date string to datetime
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            # Sort by date
            self.df = self.df.sort_values('Date')
            print(f"Loaded {len(self.df)} game records.")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def create_all_visualizations(self, output_dir="game_stats_visualizations"):
        """Create all visualizations and save to output directory"""
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate all visualizations
        self.create_win_loss_distribution(output_dir)
        self.create_unit_allocation_comparison(output_dir)
        self.create_hearts_lost_per_game(output_dir)
        self.create_player_improvement_over_time(output_dir)
        self.create_game_duration_trend(output_dir)
        self.create_battle_count_chart(output_dir)
        self.create_unit_allocation_pie_chart(output_dir)
        self.create_hearts_lost_histogram(output_dir)
        self.create_game_duration_box_plot(output_dir)
        self.create_action_type_distribution(output_dir)
        self.create_statistical_table(output_dir)

        print(f"All visualizations saved to {output_dir}")

    def create_win_loss_distribution(self, output_dir):
        """Create bar chart showing win/loss distribution for each player"""
        plt.figure(figsize=(10, 6))

        # Get all unique player names
        all_players = set(self.df['Player1'].tolist() + self.df['Player2'].tolist())
        all_players = [p for p in all_players if p != 'Enemy Castle']  # Exclude AI

        # Calculate wins for each player
        wins_data = []
        losses_data = []

        for player in all_players:
            # Count wins
            wins = len(self.df[self.df['Winner'] == player])

            # Count games played
            games_played = len(self.df[(self.df['Player1'] == player) | (self.df['Player2'] == player)])

            # Calculate losses
            losses = games_played - wins

            wins_data.append(wins)
            losses_data.append(losses)

        # Create figure
        x = np.arange(len(all_players))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))
        wins_bar = ax.bar(x - width / 2, wins_data, width, label='Wins', color='green')
        losses_bar = ax.bar(x + width / 2, losses_data, width, label='Losses', color='red')

        # Add labels and title
        ax.set_xlabel('Players', fontweight='bold')
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title('Win/Loss Distribution by Player', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(all_players)
        ax.legend()

        # Add data labels
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                if height > 0:  # Only add label if there's a value
                    ax.annotate(f'{height}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

        add_labels(wins_bar)
        add_labels(losses_bar)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/win_loss_distribution.png", dpi=300)
        plt.close()

    def create_unit_allocation_comparison(self, output_dir):
        """Create bar chart comparing soldier vs farmer allocation across games"""
        plt.figure(figsize=(12, 6))

        # Create bar chart
        x = np.arange(len(self.df))
        width = 0.35

        fig, ax = plt.subplots(figsize=(max(8, len(self.df)), 6))

        # Plot soldiers and farmers
        soldiers_bar = ax.bar(x - width / 2, self.df['SoldiersCreated'], width, label='Soldiers', color='red')
        farmers_bar = ax.bar(x + width / 2, self.df['FarmersCreated'], width, label='Farmers', color='green')

        # Add labels and title
        ax.set_xlabel('Game Number', fontweight='bold')
        ax.set_ylabel('Unit Count', fontweight='bold')
        ax.set_title('Soldier vs. Farmer Allocation Comparison by Game', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f'Game {i + 1}' for i in range(len(self.df))])
        ax.legend()

        # Add secondary labels for player names
        players_labels = [f"{row['Player1']} vs {row['Player2']}" for _, row in self.df.iterrows()]
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xticks(x)
        ax2.set_xticklabels(players_labels, rotation=45, ha='left')

        plt.tight_layout()
        plt.savefig(f"{output_dir}/unit_allocation_comparison.png", dpi=300)
        plt.close()

    def create_hearts_lost_per_game(self, output_dir):
        """Create bar chart showing hearts lost by each player per game"""
        plt.figure(figsize=(12, 6))

        # Create bar chart
        x = np.arange(len(self.df))
        width = 0.35

        fig, ax = plt.subplots(figsize=(max(8, len(self.df)), 6))

        # Plot hearts lost
        p1_bar = ax.bar(x - width / 2, self.df['HeartsLostPlayer1'], width, label='Player 1', color='blue')
        p2_bar = ax.bar(x + width / 2, self.df['HeartsLostPlayer2'], width, label='Player 2', color='orange')

        # Add labels and title
        ax.set_xlabel('Game Number', fontweight='bold')
        ax.set_ylabel('Hearts Lost', fontweight='bold')
        ax.set_title('Hearts Lost Per Game by Player', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f'Game {i + 1}' for i in range(len(self.df))])

        # Add secondary labels for player names
        players_labels = [f"{row['Player1']} vs {row['Player2']}" for _, row in self.df.iterrows()]
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xticks(x)
        ax2.set_xticklabels(players_labels, rotation=45, ha='left')

        # Add legend with player names
        player1_names = self.df['Player1'].tolist()
        player2_names = self.df['Player2'].tolist()
        ax.legend([f'Player 1 ({", ".join(set(player1_names))})',
                   f'Player 2 ({", ".join(set(player2_names))})'])

        plt.tight_layout()
        plt.savefig(f"{output_dir}/hearts_lost_per_game.png", dpi=300)
        plt.close()

    def create_player_improvement_over_time(self, output_dir):
        """Create line graph showing player improvement over time"""
        plt.figure(figsize=(12, 6))

        # Get all unique players except AI
        all_players = set(self.df['Player1'].tolist() + self.df['Player2'].tolist())
        all_players = [p for p in all_players if p != 'Enemy Castle']

        # Track win ratio for each player over time
        player_performance = {}

        for player in all_players:
            wins = []
            total_games = []
            win_ratios = []

            # Calculate cumulative win ratio over time
            for i, row in self.df.iterrows():
                # Check if this player was involved in this game
                if row['Player1'] == player or row['Player2'] == player:
                    # Update win count if player won
                    if row['Winner'] == player:
                        wins.append(1)
                    else:
                        wins.append(0)

                    # Update total games
                    total_games.append(1)

                    # Calculate win ratio so far
                    win_ratio = sum(wins) / sum(total_games)
                    win_ratios.append(win_ratio)

            # Store performance data
            if win_ratios:  # Only if player played games
                player_performance[player] = {
                    'win_ratios': win_ratios,
                    'game_indices': list(range(1, len(win_ratios) + 1))
                }

        # Plot improvement over time for each player
        fig, ax = plt.subplots(figsize=(12, 6))

        for player, data in player_performance.items():
            ax.plot(data['game_indices'], data['win_ratios'], marker='o', label=player)

        # Add labels and title
        ax.set_xlabel('Games Played', fontweight='bold')
        ax.set_ylabel('Win Ratio', fontweight='bold')
        ax.set_title('Player Win Ratio Improvement Over Time', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True)

        # Add horizontal line at 0.5 for reference
        ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/player_improvement.png", dpi=300)
        plt.close()

    def create_game_duration_trend(self, output_dir):
        """Create line graph showing trend in game duration over time"""
        plt.figure(figsize=(12, 6))

        # Prepare data
        game_indices = list(range(1, len(self.df) + 1))
        durations = self.df['GameDuration'].tolist()

        # Calculate moving average (if there are enough data points)
        window_size = min(3, len(durations))
        if window_size > 1:
            moving_avg = []
            for i in range(len(durations)):
                start_idx = max(0, i - window_size + 1)
                window_avg = sum(durations[start_idx:i + 1]) / (i - start_idx + 1)
                moving_avg.append(window_avg)

        # Plot durations and trend
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(game_indices, durations, marker='o', color='blue', label='Game Duration')

        # Add trendline
        if len(durations) > 1:
            z = np.polyfit(game_indices, durations, 1)
            p = np.poly1d(z)
            ax.plot(game_indices, p(game_indices), 'r--', label=f'Trend Line (y={z[0]:.2f}x+{z[1]:.2f})')

        # Add moving average if enough data points
        if window_size > 1:
            ax.plot(game_indices, moving_avg, 'g-', label=f'{window_size}-Game Moving Average')

        # Add labels and title
        ax.set_xlabel('Game Number', fontweight='bold')
        ax.set_ylabel('Duration (seconds)', fontweight='bold')
        ax.set_title('Game Duration Trend Over Time', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True)

        # Add labels for matchups
        matchups = [f"{row['Player1']} vs {row['Player2']}" for _, row in self.df.iterrows()]

        # If there are many games, add labels for selected games only
        if len(matchups) > 10:
            step = len(matchups) // 10 + 1
            for i in range(0, len(matchups), step):
                ax.annotate(matchups[i],
                            xy=(game_indices[i], durations[i]),
                            xytext=(0, 10),
                            textcoords="offset points",
                            ha='center',
                            fontsize=8)
        else:
            for i, matchup in enumerate(matchups):
                ax.annotate(matchup,
                            xy=(game_indices[i], durations[i]),
                            xytext=(0, 10),
                            textcoords="offset points",
                            ha='center',
                            fontsize=8)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/game_duration_trend.png", dpi=300)
        plt.close()

    def create_battle_count_chart(self, output_dir):
        """Create bar chart showing battle frequency per game"""
        plt.figure(figsize=(12, 6))

        # Prepare data
        games = [f"Game {i + 1}" for i in range(len(self.df))]
        battle_counts = self.df['BattleCount'].tolist()

        # Create bar chart
        fig, ax = plt.subplots(figsize=(max(8, len(self.df)), 6))
        bars = ax.bar(games, battle_counts, color=sns.color_palette("Blues_d", len(self.df)))

        # Add labels and title
        ax.set_xlabel('Game', fontweight='bold')
        ax.set_ylabel('Battle Count', fontweight='bold')
        ax.set_title('Battle Frequency Per Game', fontsize=14, fontweight='bold')

        # Add data labels
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        # Add average line
        avg_battles = np.mean(battle_counts)
        ax.axhline(y=avg_battles, color='r', linestyle='--', label=f'Average: {avg_battles:.1f}')

        # Add matchup labels under the bars
        matchups = [f"{row['Player1']} vs {row['Player2']}" for _, row in self.df.iterrows()]
        ax.set_xticks(range(len(games)))
        ax.set_xticklabels(games)

        # Add second x-axis for matchup names
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xticks(range(len(matchups)))
        ax2.set_xticklabels(matchups, rotation=45, ha='left')

        ax.legend()
        plt.tight_layout()
        plt.savefig(f"{output_dir}/battle_count_chart.png", dpi=300)
        plt.close()

    def create_unit_allocation_pie_chart(self, output_dir):
        """Create pie chart showing soldier vs farmer ratio"""
        plt.figure(figsize=(10, 8))

        # Calculate total soldiers and farmers across all games
        total_soldiers = self.df['SoldiersCreated'].sum()
        total_farmers = self.df['FarmersCreated'].sum()

        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 8))

        labels = ['Soldiers', 'Farmers']
        sizes = [total_soldiers, total_farmers]
        colors = ['#ff6666', '#66b266']
        explode = (0.1, 0)  # explode the soldiers slice

        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90, textprops={'fontsize': 14, 'fontweight': 'bold'})

        # Add title and ensure the pie is drawn as a circle
        ax.set_title('Soldiers vs. Farmers Allocation Ratio', fontsize=16, fontweight='bold')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Add actual numbers
        ax.text(0, -1.2, f"Total Units: {total_soldiers + total_farmers}",
                ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(-1, -1.2, f"Soldiers: {total_soldiers}",
                ha='left', va='center', fontsize=12, color=colors[0])
        ax.text(1, -1.2, f"Farmers: {total_farmers}",
                ha='right', va='center', fontsize=12, color=colors[1])

        plt.tight_layout()
        plt.savefig(f"{output_dir}/unit_allocation_pie_chart.png", dpi=300)
        plt.close()

    def create_hearts_lost_histogram(self, output_dir):
        """Create histogram showing the distribution of hearts lost"""
        plt.figure(figsize=(12, 6))

        # Gather all hearts lost data
        player1_hearts = self.df['HeartsLostPlayer1'].tolist()
        player2_hearts = self.df['HeartsLostPlayer2'].tolist()

        # Create separate histograms for player 1 and player 2
        fig, ax = plt.subplots(figsize=(12, 6))

        # Set bin range based on data
        max_hearts = max(max(player1_hearts) if player1_hearts else 0,
                         max(player2_hearts) if player2_hearts else 0)
        bins = range(0, int(max_hearts) + 5, 5)  # bins of 5 hearts

        ax.hist(player1_hearts, bins=bins, alpha=0.7, label='Player 1', color='blue')
        ax.hist(player2_hearts, bins=bins, alpha=0.7, label='Player 2', color='orange')

        # Add labels and title
        ax.set_xlabel('Hearts Lost', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Distribution of Hearts Lost by Players', fontsize=14, fontweight='bold')
        ax.legend()

        # Add grid
        ax.grid(axis='y', alpha=0.75)

        # Add statistics as text
        stats_text = (f"Player 1 Avg: {np.mean(player1_hearts):.1f} hearts\n"
                      f"Player 2 Avg: {np.mean(player2_hearts):.1f} hearts\n"
                      f"Player 1 Max: {max(player1_hearts) if player1_hearts else 0} hearts\n"
                      f"Player 2 Max: {max(player2_hearts) if player2_hearts else 0} hearts")

        # Position text in the upper right corner
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='right', bbox=props)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/hearts_lost_histogram.png", dpi=300)
        plt.close()

    def create_game_duration_box_plot(self, output_dir):
        """Create box plot showing game duration distribution"""
        plt.figure(figsize=(10, 6))

        # Create box plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Calculate game durations in minutes for better readability
        durations_min = self.df['GameDuration'] / 60

        # Create box plot
        box = ax.boxplot(durations_min, patch_artist=True, vert=False)

        # Customize box plot
        for patch in box['boxes']:
            patch.set_facecolor('#9999ff')

        # Add individual points for each game
        ax.scatter(durations_min, [1] * len(durations_min), color='red', s=50, alpha=0.6)

        # Add labels for each point
        for i, duration in enumerate(durations_min):
            ax.annotate(f"Game {i + 1}", xy=(duration, 1), xytext=(0, -15),
                        textcoords="offset points", ha='center', fontsize=8)

        # Add labels and title
        ax.set_xlabel('Game Duration (minutes)', fontweight='bold')
        ax.set_title('Game Duration Distribution', fontsize=14, fontweight='bold')

        # Remove y-axis ticks and labels
        ax.set_yticks([])

        # Add statistics as text
        stats_text = (f"Min: {min(durations_min):.1f} min\n"
                      f"Max: {max(durations_min):.1f} min\n"
                      f"Mean: {np.mean(durations_min):.1f} min\n"
                      f"Median: {np.median(durations_min):.1f} min\n")

        # Position text in the upper right corner
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='right', bbox=props)

        ax.grid(axis='x')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/game_duration_box_plot.png", dpi=300)
        plt.close()

    def create_action_type_distribution(self, output_dir):
        """Create bar chart showing action type frequency"""
        plt.figure(figsize=(12, 6))

        # Gather action type data
        action_types = ['AttackActions', 'HealActions', 'DamageBoostActions', 'CardActions']
        action_labels = ['Attack', 'Heal', 'Damage Boost', 'Card Play']
        action_counts = [self.df[col].sum() for col in action_types]

        # Create bar chart
        fig, ax = plt.subplots(figsize=(12, 6))

        # Colorful bars
        colors = ['#ff6666', '#66b266', '#6666ff', '#b266b2']
        bars = ax.bar(action_labels, action_counts, color=colors)

        # Add labels and title
        ax.set_xlabel('Action Type', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Action Type Distribution Across All Games', fontsize=14, fontweight='bold')

        # Add data labels
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        # Add percentage labels
        total_actions = sum(action_counts)
        for i, count in enumerate(action_counts):
            percentage = count / total_actions * 100 if total_actions > 0 else 0
            ax.annotate(f'{percentage:.1f}%',
                        xy=(i, count),
                        xytext=(0, -15),  # 15 points vertical offset downward
                        textcoords="offset points",
                        ha='center', va='top',
                        fontweight='bold')

        ax.grid(axis='y')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/action_type_distribution.png", dpi=300)
        plt.close()

    def create_statistical_table(self, output_dir):
        """Create a table showing statistical values for game features"""
        # Calculate statistics
        stats = {
            'Battle Count': {
                'Mean': self.df['BattleCount'].mean(),
                'Min': self.df['BattleCount'].min(),
                'Max': self.df['BattleCount'].max(),
                'StdDev': self.df['BattleCount'].std()
            },
            'Unit Allocation': {
                'Mean': (self.df['SoldiersCreated'] /
                         (self.df['SoldiersCreated'] + self.df['FarmersCreated'])).mean() * 100,
                'Min': (self.df['SoldiersCreated'] /
                        (self.df['SoldiersCreated'] + self.df['FarmersCreated'])).min() * 100,
                'Max': (self.df['SoldiersCreated'] /
                        (self.df['SoldiersCreated'] + self.df['FarmersCreated'])).max() * 100
            },
            'Hearts Lost': {
                'Mean': (self.df['HeartsLostPlayer1'] + self.df['HeartsLostPlayer2']).mean(),
                'Min': (self.df['HeartsLostPlayer1'] + self.df['HeartsLostPlayer2']).min(),
                'Max': (self.df['HeartsLostPlayer1'] + self.df['HeartsLostPlayer2']).max(),
                'StdDev': (self.df['HeartsLostPlayer1'] + self.df['HeartsLostPlayer2']).std()
            },
            'Game Duration': {
                'Mean': self.df['GameDuration'].mean(),
                'Min': self.df['GameDuration'].min(),
                'Max': self.df['GameDuration'].max(),
                'StdDev': self.df['GameDuration'].std()
            }
        }

        # Calculate win rate for each player
        all_players = set(self.df['Player1'].tolist() + self.df['Player2'].tolist())
        all_players = [p for p in all_players if p != 'Enemy Castle']  # Exclude AI

        win_rates = {}
        for player in all_players:
            games_played = len(self.df[(self.df['Player1'] == player) | (self.df['Player2'] == player)])
            wins = len(self.df[self.df['Winner'] == player])
            win_rate = (wins / games_played) * 100 if games_played > 0 else 0
            win_rates[player] = win_rate

        # Create table figure
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('tight')
        ax.axis('off')

        # Prepare table data
        table_data = []

        # Add statistics for game features
        for feature, values in stats.items():
            if 'StdDev' in values:
                row = [feature, f"{values['Mean']:.2f}", f"{values['Min']}", f"{values['Max']}",
                       f"{values['StdDev']:.2f}"]
            else:
                row = [feature, f"{values['Mean']:.2f}", f"{values['Min']}", f"{values['Max']}", "N/A"]
            table_data.append(row)

        # Add win rate for each player
        for player, rate in win_rates.items():
            table_data.append([f"{player} Win Rate", f"{rate:.2f}%", "N/A", "N/A", "N/A"])

        # Create table
        column_headers = ['Feature', 'Average', 'Min', 'Max', 'Std Dev']
        table = ax.table(cellText=table_data, colLabels=column_headers, loc='center', cellLoc='center')

        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        # Set header style
        for (i, j), cell in table.get_celld().items():
            if i == 0:  # Header row
                cell.set_text_props(fontproperties=dict(weight='bold'))
                cell.set_facecolor('#ccccff')
            elif j == 0:  # First column
                cell.set_text_props(fontproperties=dict(weight='bold'))
                cell.set_facecolor('#e6e6ff')

        # Title
        plt.suptitle('Castle War Game - Statistical Summary', fontsize=16, fontweight='bold')
        plt.figtext(0.5, 0.01, f'Generated on {datetime.now().strftime("%Y-%m-%d")}',
                    ha='center', fontsize=8)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/statistical_table.png", dpi=300, bbox_inches='tight')
        plt.close()


if __name__ == "__main__":
    visualizer = GameStatsVisualizer()
    visualizer.create_all_visualizations()
    print("Done! Check the 'game_stats_visualizations' folder for all visualizations")