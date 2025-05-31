"""
Emerald's Killfeed - Embed Factory
Advanced embed creation with themed messaging and file attachments
"""

import discord
from datetime import datetime, timezone
from pathlib import Path
import logging
import random
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class EmbedFactory:
    """Advanced embed factory with themed messaging and proper file attachment handling"""

    # Asset paths validation
    ASSETS_PATH = Path('./assets')

    # Color scheme for different embed types
    COLORS = {
        'killfeed': 0xFF4444,  # Red for kills
        'suicide': 0xFFAA00,   # Orange for suicides
        'connection': 0x00AA55, # Green for connections
        'mission': 0x5555FF,   # Blue for missions
        'airdrop': 0xFFAA55,   # Yellow for airdrops
        'helicrash': 0xFF8800, # Orange for helicrashes
        'trader': 0x8855FF,    # Purple for traders
        'vehicle': 0x888888,   # Gray for vehicles
        'success': 0x00FF00,   # Bright green for success
        'error': 0xFF0000,     # Red for errors
        'warning': 0xFFFF00,   # Yellow for warnings
        'info': 0x0099FF       # Light blue for info
    }

    # Themed message pools
    CONNECTION_TITLES = [
        "Reinforcements Confirmed",
        "Extraction Protocol Initiated", 
        "New Operative Deployment",
        "Squad Member Arrival",
        "Contact Established"
    ]

    CONNECTION_DESCRIPTIONS = [
        "A new combatant has entered the battlefield",
        "Fresh blood joins the wasteland conflict",
        "Another survivor steps into the chaos",
        "The war machine gains another operator",
        "A warrior emerges from the shadows"
    ]

    MISSION_READY_TITLES = [
        "Objective Deployment Confirmed",
        "Mission Parameters Active", 
        "Target Zone Established",
        "Operation Clearance Granted",
        "Tactical Opportunity Available"
    ]

    MISSION_READY_DESCRIPTIONS = [
        "High-value objectives await skilled operatives",
        "The battlefield offers new challenges to conquer", 
        "Strategic assets require immediate attention",
        "Critical missions demand experienced soldiers",
        "Valuable targets have been identified for extraction"
    ]

    MISSION_ACTIVE_TITLES = [
        "Operation In Progress",
        "Combat Engagement Active",
        "Tactical Mission Underway", 
        "Objective Under Assault",
        "Strike Team Deployed"
    ]

    MISSION_COMPLETE_TITLES = [
        "Mission Accomplished",
        "Objective Secured",
        "Target Neutralized",
        "Operation Successful", 
        "Victory Achieved"
    ]

    AIRDROP_TITLES = [
        "Supply Drop Inbound",
        "High-Value Cargo Incoming",
        "Emergency Resupply Detected",
        "Strategic Assets En Route",
        "Critical Supplies Deployed"
    ]

    HELICRASH_TITLES = [
        "Aircraft Down",
        "Helicopter Wreckage Located", 
        "Crash Site Identified",
        "Downed Aircraft Detected",
        "Emergency Landing Confirmed"
    ]

    TRADER_TITLES = [
        "Black Market Operative",
        "Arms Dealer Sighted",
        "Supply Contact Available",
        "Underground Merchant",
        "Resource Broker Active"
    ]

    # Mission mappings for readable names
    MISSION_MAPPINGS = {
        'GA_Airport_mis_01_SFPSACMission': 'Airport Mission #1',
        'GA_Airport_mis_02_SFPSACMission': 'Airport Mission #2',
        'GA_Airport_mis_03_SFPSACMission': 'Airport Mission #3',
        'GA_Airport_mis_04_SFPSACMission': 'Airport Mission #4',
        'GA_Military_02_Mis1': 'Military Base Mission #2',
        'GA_Military_03_Mis_01': 'Military Base Mission #3',
        'GA_Military_04_Mis1': 'Military Base Mission #4',
        'GA_Beregovoy_Mis1': 'Beregovoy Settlement Mission',
        'GA_Settle_05_ChernyLog_Mis1': 'Cherny Log Settlement Mission',
        'GA_Ind_01_m1': 'Industrial Zone Mission #1',
        'GA_Ind_02_Mis_1': 'Industrial Zone Mission #2',
        'GA_KhimMash_Mis_01': 'Chemical Plant Mission #1',
        'GA_KhimMash_Mis_02': 'Chemical Plant Mission #2',
        'GA_Bunker_01_Mis1': 'Underground Bunker Mission',
        'GA_Sawmill_01_Mis1': 'Sawmill Mission #1',
        'GA_Settle_09_Mis_1': 'Settlement Mission #9',
        'GA_Military_04_Mis_2': 'Military Base Mission #4B',
        'GA_PromZone_6_Mis_1': 'Industrial Zone Mission #6',
        'GA_PromZone_Mis_01': 'Industrial Zone Mission A',
        'GA_PromZone_Mis_02': 'Industrial Zone Mission B',
        'GA_Kamensk_Ind_3_Mis_1': 'Kamensk Industrial Mission',
        'GA_Kamensk_Mis_1': 'Kamensk City Mission #1',
        'GA_Kamensk_Mis_2': 'Kamensk City Mission #2',
        'GA_Kamensk_Mis_3': 'Kamensk City Mission #3',
        'GA_Krasnoe_Mis_1': 'Krasnoe City Mission',
        'GA_Vostok_Mis_1': 'Vostok City Mission',
        'GA_Lighthouse_02_Mis1': 'Lighthouse Mission #2',
        'GA_Elevator_Mis_1': 'Elevator Complex Mission #1',
        'GA_Elevator_Mis_2': 'Elevator Complex Mission #2',
        'GA_Sawmill_02_1_Mis1': 'Sawmill Mission #2A',
        'GA_Sawmill_03_Mis_01': 'Sawmill Mission #3',
        'GA_Bochki_Mis_1': 'Barrel Storage Mission',
        'GA_Dubovoe_0_Mis_1': 'Dubovoe Resource Mission',
    }

    @staticmethod
    def normalize_mission_name(mission_id: str) -> str:
        """Convert mission ID to readable name"""
        return EmbedFactory.MISSION_MAPPINGS.get(mission_id, mission_id.replace('_', ' ').title())

    @staticmethod
    def get_mission_level(mission_id: str) -> int:
        """Determine mission difficulty level"""
        if any(x in mission_id.lower() for x in ['airport', 'military', 'bunker']):
            return 4  # High difficulty
        elif any(x in mission_id.lower() for x in ['industrial', 'chemical', 'kamensk']):
            return 3  # Medium-high difficulty
        elif any(x in mission_id.lower() for x in ['settlement', 'sawmill']):
            return 2  # Medium difficulty
        else:
            return 1  # Low difficulty

    @staticmethod
    async def build(embed_type: str, embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build embed with proper file attachment"""
        try:
            if embed_type == 'connection':
                return await EmbedFactory.build_connection_embed(embed_data)
            elif embed_type == 'mission':
                return await EmbedFactory.build_mission_embed(embed_data)
            elif embed_type == 'airdrop':
                return await EmbedFactory.build_airdrop_embed(embed_data)
            elif embed_type == 'helicrash':
                return await EmbedFactory.build_helicrash_embed(embed_data)
            elif embed_type == 'trader':
                return await EmbedFactory.build_trader_embed(embed_data)
            elif embed_type == 'killfeed':
                return await EmbedFactory.build_killfeed_embed(embed_data)
            elif embed_type == 'leaderboard':
                return await EmbedFactory.build_leaderboard_embed(embed_data)
            elif embed_type == 'stats':
                return await EmbedFactory.build_stats_embed(embed_data)
            else:
                return await EmbedFactory.build_generic_embed(embed_data)
        except Exception as e:
            logger.error(f"Error building {embed_type} embed: {e}")
            return await EmbedFactory.build_error_embed(f"Failed to build {embed_type} embed")

    @staticmethod
    async def build_connection_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build connection embed with themed messaging"""
        try:
            # Use random themed titles and descriptions
            title = embed_data.get('title', random.choice(EmbedFactory.CONNECTION_TITLES))
            description = embed_data.get('description', random.choice(EmbedFactory.CONNECTION_DESCRIPTIONS))
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=EmbedFactory.COLORS['connection'],
                timestamp=datetime.now(timezone.utc)
            )

            player_name = embed_data.get('player_name', 'Unknown Player')
            platform = embed_data.get('platform', 'Unknown')
            server_name = embed_data.get('server_name', 'Unknown Server')

            embed.add_field(name="Operative", value=player_name, inline=True)
            embed.add_field(name="Platform", value=platform, inline=True)
            embed.add_field(name="Deployment Zone", value=server_name, inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            # Create file attachment
            connections_file = discord.File("./assets/Connections.png", filename="Connections.png")
            embed.set_thumbnail(url="attachment://Connections.png")

            return embed, connections_file

        except Exception as e:
            logger.error(f"Error building connection embed: {e}")
            return await EmbedFactory.build_error_embed("Connection embed error")

    @staticmethod
    async def build_mission_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build mission embed with difficulty indicators"""
        try:
            mission_id = embed_data.get('mission_id', '')
            state = embed_data.get('state', 'UNKNOWN')
            level = embed_data.get('level', 1)

            # Mission state specific titles and colors using themed messaging
            if state == 'READY':
                title = random.choice(EmbedFactory.MISSION_READY_TITLES)
                description = random.choice(EmbedFactory.MISSION_READY_DESCRIPTIONS)
                color = EmbedFactory.COLORS['mission']
            elif state == 'IN_PROGRESS':
                title = random.choice(EmbedFactory.MISSION_ACTIVE_TITLES)
                description = "Elite operatives are currently engaging the target"
                color = 0xFFAA00  # Orange for active
            elif state == 'COMPLETED':
                title = random.choice(EmbedFactory.MISSION_COMPLETE_TITLES)
                description = "The operation has been successfully executed"
                color = EmbedFactory.COLORS['success']
            else:
                title = "Mission Status Update"
                description = "Tactical situation has evolved"
                color = EmbedFactory.COLORS['info']

            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )

            # Mission details with military styling
            mission_name = EmbedFactory.normalize_mission_name(mission_id)
            embed.add_field(name="Target Designation", value=mission_name, inline=False)

            # Difficulty indicator without emojis
            threat_levels = ["Low", "Medium", "High", "Critical"]
            threat_level = threat_levels[min(level-1, 3)] if level > 0 else "Unknown"
            embed.add_field(name="Threat Level", value=f"Class {level} - {threat_level}", inline=True)
            embed.add_field(name="Operation Status", value=state.replace('_', ' ').title(), inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            # Create file attachment
            mission_file = discord.File("./assets/Mission.png", filename="Mission.png")
            embed.set_thumbnail(url="attachment://Mission.png")

            return embed, mission_file

        except Exception as e:
            logger.error(f"Error building mission embed: {e}")
            return await EmbedFactory.build_error_embed("Mission embed error")

    @staticmethod
    async def build_airdrop_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build airdrop embed"""
        try:
            title = random.choice(EmbedFactory.AIRDROP_TITLES)
            embed = discord.Embed(
                title=title,
                description="Critical military assets are being delivered to the operational zone",
                color=EmbedFactory.COLORS['airdrop'],
                timestamp=datetime.now(timezone.utc)
            )

            location = embed_data.get('location', 'Unknown Location')
            embed.add_field(name="Drop Zone", value=location, inline=True)
            embed.add_field(name="Cargo Status", value="Inbound", inline=True)
            embed.add_field(name="Asset Classification", value="High-Value Military Supplies", inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            # Create file attachment
            airdrop_file = discord.File("./assets/Airdrop.png", filename="Airdrop.png")
            embed.set_thumbnail(url="attachment://Airdrop.png")

            return embed, airdrop_file

        except Exception as e:
            logger.error(f"Error building airdrop embed: {e}")
            return await EmbedFactory.build_error_embed("Airdrop embed error")

    @staticmethod
    async def build_helicrash_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build helicrash embed"""
        try:
            title = random.choice(EmbedFactory.HELICRASH_TITLES)
            embed = discord.Embed(
                title=title,
                description="Military aviation asset has been compromised in hostile territory",
                color=EmbedFactory.COLORS['helicrash'],
                timestamp=datetime.now(timezone.utc)
            )

            location = embed_data.get('location', 'Unknown Location')
            embed.add_field(name="Crash Coordinates", value=location, inline=True)
            embed.add_field(name="Recovery Status", value="Site Located", inline=True)
            embed.add_field(name="Asset Classification", value="Military Hardware", inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            # Create file attachment
            helicrash_file = discord.File("./assets/Helicrash.png", filename="Helicrash.png")
            embed.set_thumbnail(url="attachment://Helicrash.png")

            return embed, helicrash_file

        except Exception as e:
            logger.error(f"Error building helicrash embed: {e}")
            return await EmbedFactory.build_error_embed("Helicrash embed error")

    @staticmethod
    async def build_trader_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build trader embed"""
        try:
            title = random.choice(EmbedFactory.TRADER_TITLES)
            embed = discord.Embed(
                title=title,
                description="Underground supply network has established contact in your sector",
                color=EmbedFactory.COLORS['trader'],
                timestamp=datetime.now(timezone.utc)
            )

            location = embed_data.get('location', 'Unknown Location')
            embed.add_field(name="Contact Location", value=location, inline=True)
            embed.add_field(name="Network Status", value="Active", inline=True)
            embed.add_field(name="Available Assets", value="Combat Equipment & Resources", inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            # Create file attachment
            trader_file = discord.File("./assets/Trader.png", filename="Trader.png")
            embed.set_thumbnail(url="attachment://Trader.png")

            return embed, trader_file

        except Exception as e:
            logger.error(f"Error building trader embed: {e}")
            return await EmbedFactory.build_error_embed("Trader embed error")

    @staticmethod
    async def build_killfeed_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build killfeed embed with themed messaging"""
        try:
            is_suicide = embed_data.get('is_suicide', False)
            weapon = embed_data.get('weapon', 'Unknown')
            distance = embed_data.get('distance', 0)

            if is_suicide:
                # Suicide embed
                player_name = embed_data.get('player_name') or embed_data.get('victim', 'Unknown Player')

                embed = discord.Embed(
                    title="💀 Fatal Incident",
                    description=f"**{player_name}** met an unfortunate end",
                    color=EmbedFactory.COLORS['suicide'],
                    timestamp=datetime.now(timezone.utc)
                )

                embed.add_field(name="👤 Player", value=player_name, inline=True)
                embed.add_field(name="⚰️ Cause", value=weapon, inline=True)
                embed.add_field(name="📊 Type", value="Self-Elimination", inline=True)

                # Use appropriate asset based on cause
                if weapon.lower() == 'falling':
                    asset_file = discord.File("./assets/Falling.png", filename="Falling.png")
                    embed.set_thumbnail(url="attachment://Falling.png")
                else:
                    asset_file = discord.File("./assets/Suicide.png", filename="Suicide.png")
                    embed.set_thumbnail(url="attachment://Suicide.png")

            else:
                # PvP kill embed
                killer = embed_data.get('killer', 'Unknown')
                victim = embed_data.get('victim', 'Unknown')
                killer_kdr = embed_data.get('killer_kdr', '0.00')
                victim_kdr = embed_data.get('victim_kdr', '0.00')

                embed = discord.Embed(
                    title="⚔️ Combat Engagement",
                    description=f"**{killer}** eliminated **{victim}**",
                    color=EmbedFactory.COLORS['killfeed'],
                    timestamp=datetime.now(timezone.utc)
                )

                embed.add_field(name="🗡️ Killer", value=f"{killer}\n`KDR: {killer_kdr}`", inline=True)
                embed.add_field(name="💀 Victim", value=f"{victim}\n`KDR: {victim_kdr}`", inline=True)
                embed.add_field(name="🔫 Weapon", value=weapon, inline=True)

                if distance > 0:
                    embed.add_field(name="📏 Distance", value=f"{distance:.1f}m", inline=True)

                asset_file = discord.File("./assets/Killfeed.png", filename="Killfeed.png")
                embed.set_thumbnail(url="attachment://Killfeed.png")

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed, asset_file

        except Exception as e:
            logger.error(f"Error building killfeed embed: {e}")
            return await EmbedFactory.build_error_embed("Killfeed embed error")

    @staticmethod
    async def build_leaderboard_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build leaderboard embed with themed messaging"""
        try:
            embed = discord.Embed(
                title=embed_data.get('title', '🏆 Leaderboard'),
                description=embed_data.get('description', 'Top players'),
                color=EmbedFactory.COLORS['info'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            main_file = discord.File("./assets/Leaderboard.png", filename="Leaderboard.png")
            embed.set_thumbnail(url="attachment://Leaderboard.png")

            return embed, main_file

        except Exception as e:
            logger.error(f"Error building leaderboard embed: {e}")
            return await EmbedFactory.build_error_embed("Leaderboard embed error")

    @staticmethod
    async def build_stats_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build stats embed with themed messaging"""
        try:
            embed = discord.Embed(
                title=embed_data.get('title', '📊 Player Stats'),
                description=embed_data.get('description', 'Player statistics'),
                color=EmbedFactory.COLORS['info'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            main_file = discord.File("./assets/WeaponStats.png", filename="WeaponStats.png")
            embed.set_thumbnail(url="attachment://WeaponStats.png")

            return embed, main_file

        except Exception as e:
            logger.error(f"Error building stats embed: {e}")
            return await EmbedFactory.build_error_embed("Stats embed error")

    @staticmethod
    async def build_generic_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build generic embed with main.png"""
        try:
            embed = discord.Embed(
                title=embed_data.get('title', 'Emerald Servers'),
                description=embed_data.get('description', 'Event notification'),
                color=EmbedFactory.COLORS['info'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            main_file = discord.File("./assets/main.png", filename="main.png")
            embed.set_thumbnail(url="attachment://main.png")

            return embed, main_file

        except Exception as e:
            logger.error(f"Error building generic embed: {e}")
            return await EmbedFactory.build_error_embed("Generic embed error")

    @staticmethod
    async def build_error_embed(error_message: str) -> tuple[discord.Embed, discord.File]:
        """Build error embed"""
        try:
            embed = discord.Embed(
                title="❌ Error",
                description=error_message,
                color=EmbedFactory.COLORS['error'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            main_file = discord.File("./assets/main.png", filename="main.png")
            embed.set_thumbnail(url="attachment://main.png")

            return embed, main_file

        except Exception as e:
            logger.error(f"Critical error building error embed: {e}")
            # Fallback embed with default file
            embed = discord.Embed(
                title="Critical Error",
                description="Multiple errors occurred",
                color=0xFF0000,
                timestamp=datetime.now(timezone.utc)
            )
            fallback_file = discord.File("./assets/main.png", filename="main.png")
            return embed, fallback_file

    @staticmethod
    def create_mission_embed(title: str, description: str, mission_id: str, level: int, state: str, respawn_time: int = None) -> discord.Embed:
        """Create mission embed (legacy compatibility)"""
        try:
            if state == 'READY':
                color = EmbedFactory.COLORS['mission']
            elif state == 'IN_PROGRESS':
                color = 0xFFAA00  # Orange
            elif state == 'COMPLETED':
                color = EmbedFactory.COLORS['success']
            else:
                color = EmbedFactory.COLORS['info']

            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )

            mission_name = EmbedFactory.normalize_mission_name(mission_id)
            embed.add_field(name="📍 Mission", value=mission_name, inline=False)

            difficulty_stars = "⭐" * level
            embed.add_field(name="💀 Difficulty", value=f"Level {level} {difficulty_stars}", inline=True)
            embed.add_field(name="📊 Status", value=state.replace('_', ' ').title(), inline=True)

            if respawn_time:
                embed.add_field(name="⏰ Respawn", value=f"{respawn_time}s", inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            embed.set_thumbnail(url="attachment://Mission.png")

            return embed

        except Exception as e:
            logger.error(f"Error creating mission embed: {e}")
            return discord.Embed(title="Error", description="Failed to create mission embed", color=0xFF0000)

    @staticmethod
    def create_airdrop_embed(state: str, location: str, timestamp: datetime) -> discord.Embed:
        """Create airdrop embed (legacy compatibility)"""
        try:
            embed = discord.Embed(
                title="🪂 Airdrop Incoming",
                description="High-value supply drop detected inbound",
                color=EmbedFactory.COLORS['airdrop'],
                timestamp=timestamp
            )

            embed.add_field(name="📍 Drop Zone", value=location, inline=True)
            embed.add_field(name="⏰ Status", value=state.title(), inline=True)
            embed.add_field(name="💰 Contents", value="High-Value Loot", inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            embed.set_thumbnail(url="attachment://Airdrop.png")

            return embed

        except Exception as e:
            logger.error(f"Error creating airdrop embed: {e}")
            return discord.Embed(title="Error", description="Failed to create airdrop embed", color=0xFF0000)

    @staticmethod
    def create_helicrash_embed(location: str, timestamp: datetime) -> discord.Embed:
        """Create helicrash embed (legacy compatibility)"""
        try:
            embed = discord.Embed(
                title="🚁 Helicopter Crash",
                description="Military helicopter has crashed - salvage opportunity detected",
                color=EmbedFactory.COLORS['helicrash'],
                timestamp=timestamp
            )

            embed.add_field(name="💥 Crash Site", value=location, inline=True)
            embed.add_field(name="⚠️ Status", value="Active", inline=True)
            embed.add_field(name="🎖️ Loot Type", value="Military Equipment", inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            embed.set_thumbnail(url="attachment://Helicrash.png")

            return embed

        except Exception as e:
            logger.error(f"Error creating helicrash embed: {e}")
            return discord.Embed(title="Error", description="Failed to create helicrash embed", color=0xFF0000)

    @staticmethod
    def create_trader_embed(location: str, timestamp: datetime) -> discord.Embed:
        """Create trader embed (legacy compatibility)"""
        try:
            embed = discord.Embed(
                title="🏪 Trader Arrival",
                description="Traveling merchant has arrived with rare goods",
                color=EmbedFactory.COLORS['trader'],
                timestamp=timestamp
            )

            embed.add_field(name="📍 Location", value=location, inline=True)
            embed.add_field(name="⏰ Status", value="Open for Business", inline=True)
            embed.add_field(name="💎 Inventory", value="Rare Items Available", inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            embed.set_thumbnail(url="attachment://Trader.png")

            return embed

        except Exception as e:
            logger.error(f"Error creating trader embed: {e}")
            return discord.Embed(title="Error", description="Failed to create trader embed", color=0xFF0000)