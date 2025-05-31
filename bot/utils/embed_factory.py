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
        'killfeed': 0xFFFF00,  # Yellow for kills
        'suicide': 0xFF0000,   # Red for suicides
        'falling': 0x8B00FF,   # Purple for falling
        'connection': 0x00AA55, # Green for connections
        'mission': 0x5555FF,   # Blue for missions
        'airdrop': 0xFFAA55,   # Yellow for airdrops
        'helicrash': 0xFF8800, # Orange for helicrashes
        'trader': 0x8855FF,    # Purple for traders
        'vehicle': 0x888888,   # Gray for vehicles
        'success': 0x00FF00,   # Bright green for success
        'error': 0xFF0000,     # Red for errors
        'warning': 0xFFFF00,   # Yellow for warnings
        'info': 0x0099FF,       # Light blue for info
        'bounty': 0xFFA500,     # Orange for bounties
        'economy': 0x32CD32      # LimeGreen for economy
    }

    # Themed message pools
    CONNECTION_TITLES = [
        "Reinforcements Confirmed",
        "Extraction Protocol Initiated", 
        "New Operative Deployment",
        "Squad Member Arrival",
        "Contact Established",
        "Survivor Integration Protocol",
        "Field Asset Mobilization",
        "Wasteland Conscription Active",
        "Combat Personnel Enlisted",
        "Ghost Protocol Activated"
    ]

    CONNECTION_DESCRIPTIONS = [
        "A new combatant has entered the battlefield",
        "Fresh blood joins the wasteland conflict",
        "Another survivor steps into the chaos",
        "The war machine gains another operator",
        "A warrior emerges from the shadows",
        "Hope arrives wrapped in kevlar and desperation",
        "The endless grind claims another soul",
        "Flesh meets metal in the machine of war",
        "Another name added to tomorrow's casualty list",
        "The hunger for conflict finds new meat"
    ]

    MISSION_READY_TITLES = [
        "Objective Deployment Confirmed",
        "Mission Parameters Active", 
        "Target Zone Established",
        "Operation Clearance Granted",
        "Tactical Opportunity Available",
        "Blood Contract Initiated",
        "Death Warrant Authorized",
        "Slaughter Protocol Engaged",
        "Carnage Clearance Obtained",
        "Extinction Event Scheduled"
    ]

    MISSION_READY_DESCRIPTIONS = [
        "High-value objectives await skilled operatives",
        "The battlefield offers new challenges to conquer", 
        "Strategic assets require immediate attention",
        "Critical missions demand experienced soldiers",
        "Valuable targets have been identified for extraction",
        "Fresh graves need digging in contested territory",
        "The meat grinder requires premium feeding",
        "Death calls for volunteers with steady hands",
        "Violence waits patiently for willing participants",
        "Glory and gore intermingle in equal measure"
    ]

    MISSION_ACTIVE_TITLES = [
        "Operation In Progress",
        "Combat Engagement Active",
        "Tactical Mission Underway", 
        "Objective Under Assault",
        "Strike Team Deployed",
        "Hellfire Protocol Executing",
        "Apocalypse Engine Running",
        "Bloodbath Initiative Active",
        "Scorched Earth Operations",
        "Devastation Protocols Engaged"
    ]

    MISSION_COMPLETE_TITLES = [
        "Mission Accomplished",
        "Objective Secured",
        "Target Neutralized",
        "Operation Successful", 
        "Victory Achieved",
        "Carnage Quota Fulfilled",
        "Death Toll Satisfied",
        "Scoreboard Updated",
        "Body Count Verified",
        "Blood Debt Collected"
    ]

    AIRDROP_TITLES = [
        "Supply Drop Inbound",
        "High-Value Cargo Incoming",
        "Emergency Resupply Detected",
        "Strategic Assets En Route",
        "Critical Supplies Deployed",
        "Salvation from the Skies",
        "Angel of Death Delivery",
        "Last Hope Package",
        "Divine Intervention Dropping",
        "Mercy Cargo Inbound"
    ]

    HELICRASH_TITLES = [
        "Aircraft Down",
        "Helicopter Wreckage Located", 
        "Crash Site Identified",
        "Downed Aircraft Detected",
        "Emergency Landing Confirmed",
        "Metal Bird Falls Silent",
        "Sky Chariot Broken",
        "Iron Angel Grounded",
        "Flying Coffin Confirmed",
        "Mechanical Vulture Downed"
    ]

    TRADER_TITLES = [
        "Black Market Operative",
        "Arms Dealer Sighted",
        "Supply Contact Available",
        "Underground Merchant",
        "Resource Broker Active",
        "Death Merchant Arrived",
        "Scavenger Lord Present",
        "Wasteland Capitalist",
        "Profiteer of Chaos",
        "Blood Money Banker"
    ]

    # Killfeed themed messages - expanded to 10
    KILL_TITLES = [
        "Combat Engagement Complete",
        "Target Eliminated",
        "Hostile Neutralized",
        "Enemy Operator Down",
        "Combat Victory Confirmed",
        "Life Debt Collected",
        "Final Transaction Processed",
        "Mortality Reminder Delivered",
        "Pulse Check Failed",
        "Breathing Privileges Revoked"
    ]

    # Kill random messages for variety
    KILL_MESSAGES = [
        "Another heartbeat silenced beneath the ash sky.",
        "No burial, no name — just silence where a soul once stood.",
        "Left no echo. Just scattered gear and cooling blood.",
        "Cut from the world like thread from a fraying coat.",
        "Hunger, cold, bullets — it could've been any of them. It was enough.",
        "Marked, hunted, forgotten. In that order.",
        "Their fire went out before they even knew they were burning.",
        "A last breath swallowed by wind and war.",
        "The price of survival paid in someone else's blood.",
        "The map didn't change. The player did."
    ]

    SUICIDE_TITLES = [
        "Casualty Report",
        "Operator Down",
        "Fatal Incident",
        "Combat Loss",
        "KIA Confirmed",
        "Self-Termination Executed",
        "Internal Error Fatal",
        "Friendly Fire Confirmed",
        "System Malfunction Critical",
        "User Input Error"
    ]

    # Menu suicide random messages
    SUICIDE_MESSAGES = [
        "Hit \"relocate\" like it was the snooze button. Got deleted.",
        "Tactical redeployment... into the abyss.",
        "Rage respawned and logic respawned with it.",
        "Wanted a reset. Got a reboot straight to the void.",
        "Pressed something. Paid everything.",
        "Who needs enemies when you've got bad decisions?",
        "Alt+F4'd themselves into Valhalla.",
        "Strategic death — poorly executed.",
        "Fast travel without a destination.",
        "Confirmed: the dead menu is not a safe zone."
    ]

    # Falling death titles
    FALLING_TITLES = [
        "Gravity Enforcement",
        "Altitude Adjustment Fatal",
        "Terminal Velocity Achieved",
        "Ground Impact Confirmed",
        "Elevation Error Corrected",
        "Physics Lesson Concluded",
        "Descent Protocol Failed",
        "Vertical Miscalculation",
        "Flight Plan Terminated",
        "Landing Coordinates Incorrect"
    ]

    # Falling random messages
    FALLING_MESSAGES = [
        "Thought they could make it. The ground disagreed.",
        "Airborne ambition. Terminal results.",
        "Tried flying. Landed poorly.",
        "Gravity called. They answered — headfirst.",
        "Believed in themselves. Gravity didn't.",
        "From rooftops to regret in under two seconds.",
        "The sky opened. The floor closed.",
        "Survival instincts took a coffee break.",
        "Feet first into a bad decision.",
        "Their plan had one fatal step too many."
    ]

    SUICIDE_DESCRIPTIONS = [
        "Operative eliminated by environmental hazards",
        "Combat casualty due to tactical error",
        "Field operative lost to hostile conditions",
        "Soldier eliminated by battlefield hazards"
    ]

    # Economy themed messages
    ECONOMY_SUCCESS_TITLES = [
        "Transaction Completed",
        "Resource Exchange Successful",
        "Asset Transfer Confirmed",
        "Economic Operation Complete",
        "Financial Transaction Processed",
        "Wealth Redistribution Active",
        "Capital Flow Authorized",
        "Investment Return Confirmed",
        "Profit Margin Secured",
        "Economic Victory Achieved"
    ]

    ECONOMY_ERROR_TITLES = [
        "Transaction Failed",
        "Insufficient Resources",
        "Operation Denied",
        "Access Restricted",
        "Authorization Required",
        "Economic Sanctions Applied",
        "Market Crash Detected",
        "Poverty Protocols Engaged",
        "Financial Quarantine Active",
        "Credit Score Obliterated"
    ]

    # Leaderboard themed messages
    LEADERBOARD_TITLES = [
        "Combat Effectiveness Rankings",
        "Tactical Performance Analysis",
        "Operator Efficiency Report",
        "Battle Statistics Summary",
        "Combat Performance Index",
        "Death Dealer Standings",
        "Survival Hierarchy Report",
        "Wasteland Who's Who",
        "Elite Eliminator Rankings",
        "Apex Predator Census"
    ]

    # Stats themed messages
    STATS_TITLES = [
        "Operator Profile",
        "Combat Record Analysis",
        "Performance Metrics",
        "Tactical Assessment",
        "Service Record",
        "Psychological Evaluation",
        "Lethality Documentation",
        "Survivor Case Study",
        "Combat Efficiency Audit",
        "Battlefield Biography"
    ]

    # Bounty themed messages
    BOUNTY_TITLES = [
        "High-Value Target",
        "Bounty Contract Active",
        "Elimination Order",
        "Target Acquisition",
        "Priority Elimination",
        "Death Warrant Issued",
        "Assassination Contract",
        "Termination Authorization",
        "Execution Order Confirmed",
        "Hunter's Mark Applied"
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
            elif embed_type == 'bounty_set':
                return await EmbedFactory.build_bounty_set_embed(embed_data)
            elif embed_type == 'bounty_list':
                return await EmbedFactory.build_bounty_list_embed(embed_data)
            elif embed_type == 'faction_created':
                return await EmbedFactory.build_faction_created_embed(embed_data)
            elif embed_type == 'economy_balance':
                return await EmbedFactory.build_economy_balance_embed(embed_data)
            elif embed_type == 'economy_work':
                return await EmbedFactory.build_economy_work_embed(embed_data)
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
                # Determine if it's falling or menu suicide and use appropriate styling
                player_name = embed_data.get('player_name') or embed_data.get('victim', 'Unknown Player')

                if weapon.lower() == 'falling':
                    # Falling death with purple color and falling titles/messages
                    title = random.choice(EmbedFactory.FALLING_TITLES)
                    color = EmbedFactory.COLORS['falling']
                    themed_description = random.choice(EmbedFactory.FALLING_MESSAGES)
                    asset_file = discord.File("./assets/Falling.png", filename="Falling.png")
                    thumbnail_url = "attachment://Falling.png"
                else:
                    # Menu suicide with red color and suicide titles/messages
                    title = random.choice(EmbedFactory.SUICIDE_TITLES)
                    color = EmbedFactory.COLORS['suicide']
                    themed_description = random.choice(EmbedFactory.SUICIDE_MESSAGES)
                    asset_file = discord.File("./assets/Suicide.png", filename="Suicide.png")
                    thumbnail_url = "attachment://Suicide.png"

                embed = discord.Embed(
                    title=title,
                    color=color,
                    timestamp=datetime.now(timezone.utc)
                )

                embed.add_field(name="Operative", value=player_name, inline=True)
                embed.add_field(name="Cause of Death", value=weapon, inline=True)
                embed.add_field(name="Status", value="KIA - Non-Combat", inline=True)

                # Add themed description at bottom (full-width)
                embed.add_field(name="Mission Report", value=themed_description, inline=False)

                embed.set_thumbnail(url=thumbnail_url)

            else:
                # PvP kill embed with yellow color and random kill messages
                killer = embed_data.get('killer', 'Unknown')
                victim = embed_data.get('victim', 'Unknown')
                killer_kdr = embed_data.get('killer_kdr', '0.00')
                victim_kdr = embed_data.get('victim_kdr', '0.00')
                title = random.choice(EmbedFactory.KILL_TITLES)

                embed = discord.Embed(
                    title=title,
                    color=EmbedFactory.COLORS['killfeed'],  # Now yellow
                    timestamp=datetime.now(timezone.utc)
                )

                embed.add_field(name="Victor", value=f"{killer}\nEfficiency: {killer_kdr}", inline=True)
                embed.add_field(name="Eliminated", value=f"{victim}\nEfficiency: {victim_kdr}", inline=True)
                embed.add_field(name="Weapon System", value=weapon, inline=True)

                if distance > 0:
                    embed.add_field(name="Engagement Range", value=f"{distance:.1f}m", inline=True)

                # Add random kill message at bottom (full-width)
                kill_message = random.choice(EmbedFactory.KILL_MESSAGES)
                embed.add_field(name="Combat Report", value=kill_message, inline=False)

                asset_file = discord.File("./assets/Killfeed.png", filename="Killfeed.png")
                embed.set_thumbnail(url="attachment://Killfeed.png")

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed, asset_file

        except Exception as e:
            logger.error(f"Error building killfeed embed: {e}")
            return await EmbedFactory.build_error_embed("Killfeed embed error")

    @staticmethod
    async def build_leaderboard_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build leaderboard embed with themed messaging and real data"""
        try:
            title = embed_data.get('title', random.choice(EmbedFactory.LEADERBOARD_TITLES))
            description = embed_data.get('description', 'Elite operators ranked by battlefield performance')

            embed = discord.Embed(
                title=title,
                description=description,
                color=EmbedFactory.COLORS['info'],
                timestamp=datetime.now(timezone.utc)
            )

            # Add real leaderboard rankings
            rankings = embed_data.get('rankings', '')
            if rankings:
                embed.add_field(name="Rankings", value=rankings, inline=False)

            # Add summary statistics if available
            total_kills = embed_data.get('total_kills', 0)
            total_deaths = embed_data.get('total_deaths', 0)
            stat_type = embed_data.get('stat_type', 'general')

            if total_kills > 0 or total_deaths > 0:
                if stat_type == 'kills':
                    embed.add_field(name="Total Eliminations", value=f"{total_kills:,}", inline=True)
                elif stat_type == 'deaths':
                    embed.add_field(name="Total Casualties", value=f"{total_deaths:,}", inline=True)
                elif stat_type == 'kdr':
                    total_kdr = total_kills / max(total_deaths, 1) if total_deaths > 0 else total_kills
                    embed.add_field(name="Average Efficiency", value=f"{total_kdr:.2f}", inline=True)

            # Add server context
            server_name = embed_data.get('server_name', 'All Servers')
            embed.add_field(name="Theater of Operations", value=server_name, inline=True)

            # Get appropriate thumbnail based on leaderboard type
            thumbnail_url = embed_data.get('thumbnail_url', 'attachment://Leaderboard.png')

            # Determine asset file based on thumbnail URL
            if 'WeaponStats.png' in thumbnail_url:
                asset_file = discord.File("./assets/WeaponStats.png", filename="WeaponStats.png")
            elif 'Faction.png' in thumbnail_url:
                asset_file = discord.File("./assets/Faction.png", filename="Faction.png")
            else:
                asset_file = discord.File("./assets/Leaderboard.png", filename="Leaderboard.png")

            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            return embed, asset_file

        except Exception as e:
            logger.error(f"Error building leaderboard embed: {e}")
            return await EmbedFactory.build_error_embed("Leaderboard embed error")

    @staticmethod
    async def build_stats_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build stats embed with themed messaging and real data"""
        try:
            player_name = embed_data.get('player_name', 'Unknown Player')
            server_name = embed_data.get('server_name', 'Unknown Server')

            title = random.choice(EmbedFactory.STATS_TITLES)
            description = f"Comprehensive battlefield performance analysis for **{player_name}**"

            embed = discord.Embed(
                title=title,
                description=description,
                color=EmbedFactory.COLORS['info'],
                timestamp=datetime.now(timezone.utc)
            )

            # Validate and use real statistics data with clean military styling
            kills = max(0, embed_data.get('kills', 0))
            deaths = max(0, embed_data.get('deaths', 0))
            kdr_value = embed_data.get('kdr', '0.00')

            # Ensure KDR is properly formatted
            try:
                if isinstance(kdr_value, (int, float)):
                    kdr = f"{float(kdr_value):.2f}"
                else:
                    kdr = str(kdr_value)
            except:
                kdr = "0.00"

            embed.add_field(name="Eliminations", value=f"{kills:,}", inline=True)
            embed.add_field(name="Casualties", value=f"{deaths:,}", inline=True)
            embed.add_field(name="Combat Efficiency", value=kdr, inline=True)

            # Additional combat metrics with validation
            personal_best_distance = float(embed_data.get('personal_best_distance', 0.0))
            favorite_weapon = embed_data.get('favorite_weapon')
            best_streak = max(0, embed_data.get('best_streak', 0))
            suicides = max(0, embed_data.get('suicides', 0))

            if personal_best_distance > 0:
                if personal_best_distance >= 1000:
                    distance_str = f"{personal_best_distance/1000:.1f}km"
                else:
                    distance_str = f"{personal_best_distance:.0f}m"
                embed.add_field(name="Longest Engagement", value=distance_str, inline=True)

            if favorite_weapon and favorite_weapon != 'None' and favorite_weapon.strip():
                embed.add_field(name="Preferred Arsenal", value=favorite_weapon, inline=True)

            if best_streak > 0:
                embed.add_field(name="Peak Performance", value=f"{best_streak:,} Streak", inline=True)

            # Add additional metrics if available
            if suicides > 0:
                embed.add_field(name="Non-Combat Losses", value=f"{suicides:,}", inline=True)

            # Server information
            embed.add_field(name="Theater of Operations", value=server_name, inline=False)

            # Add tactical summary at bottom with enhanced messaging
            if kills > 0 or deaths > 0:
                total_engagements = kills + deaths
                survival_rate = (kills / total_engagements * 100) if total_engagements > 0 else 0

                if survival_rate >= 70:
                    performance_rank = "Elite Operative"
                elif survival_rate >= 50:
                    performance_rank = "Veteran Soldier"
                elif survival_rate >= 30:
                    performance_rank = "Experienced Fighter"
                else:
                    performance_rank = "Active Combatant"

                embed.add_field(name="Tactical Assessment", 
                               value=f"**{performance_rank}** • {total_engagements:,} total engagements • {survival_rate:.1f}% victory rate", 
                               inline=False)

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
    async def build_bounty_set_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build bounty set embed"""
        try:
            title = random.choice(EmbedFactory.BOUNTY_TITLES)

            embed = discord.Embed(
                title=title,
                description=f"Contract established on **{embed_data['target_character']}**",
                color=EmbedFactory.COLORS['bounty'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="Reward", value=f"${embed_data['bounty_amount']:,}", inline=True)
            embed.add_field(name="Target", value=embed_data['target_character'], inline=True)
            embed.add_field(name="Expires", value=f"<t:{embed_data['expires_timestamp']}:R>", inline=True)
            embed.add_field(name="Instructions", value="Eliminate target to claim bounty", inline=False)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            bounty_file = discord.File("./assets/Bounty.png", filename="Bounty.png")
            embed.set_thumbnail(url="attachment://Bounty.png")

            return embed, bounty_file

        except Exception as e:
            logger.error(f"Error building bounty set embed: {e}")
            return await EmbedFactory.build_error_embed("Bounty set embed error")

    @staticmethod
    async def build_bounty_list_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build bounty list embed"""
        try:
            title = random.choice(EmbedFactory.BOUNTY_TITLES)

            embed = discord.Embed(
                title="Priority Elimination Contracts",
                description=f"**{embed_data['total_bounties']}** active contracts",
                color=EmbedFactory.COLORS['bounty'],
                timestamp=datetime.now(timezone.utc)
            )

            bounty_list = []
            for i, bounty in enumerate(embed_data['bounty_list'], 1):
                target = bounty['target_character']
                amount = bounty['amount']
                expires = bounty['expires_at']
                auto_indicator = " [AUTO]" if bounty.get('auto_generated', False) else ""

                bounty_list.append(
                    f"**{i}.** {target} - ${amount:,}{auto_indicator}\n"
                    f"    Expires <t:{int(expires.timestamp())}:R>"
                )

            embed.add_field(name="Active Contracts", value="\n".join(bounty_list), inline=False)

            if embed_data.get('showing_partial'):
                embed.add_field(name="Status", value=f"Showing top 10 contracts", inline=False)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            bounty_file = discord.File("./assets/Bounty.png", filename="Bounty.png")
            embed.set_thumbnail(url="attachment://Bounty.png")

            return embed, bounty_file

        except Exception as e:
            logger.error(f"Error building bounty list embed: {e}")
            return await EmbedFactory.build_error_embed("Bounty list embed error")

    @staticmethod
    async def build_faction_created_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build faction created embed"""
        try:
            embed = discord.Embed(
                title="Faction Established",
                description=f"Successfully created faction **{embed_data['faction_name']}**",
                color=EmbedFactory.COLORS['success'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="Leader", value=embed_data['leader'], inline=True)

            if embed_data.get('faction_tag'):
                embed.add_field(name="Tag", value=f"[{embed_data['faction_tag']}]", inline=True)

            embed.add_field(
                name="Members", 
                value=f"{embed_data['member_count']}/{embed_data['max_members']}", 
                inline=True
            )

            embed.add_field(
                name="Next Steps", 
                value="Use /faction invite to recruit members\nUse /faction settings to configure options", 
                inline=False
            )

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            faction_file = discord.File("./assets/Faction.png", filename="Faction.png")
            embed.set_thumbnail(url="attachment://Faction.png")

            return embed, faction_file

        except Exception as e:
            logger.error(f"Error building faction created embed: {e}")
            return await EmbedFactory.build_error_embed("Faction creation embed error")

    @staticmethod
    async def build_economy_balance_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build economy balance embed"""
        try:
            title = random.choice(EmbedFactory.ECONOMY_SUCCESS_TITLES)

            embed = discord.Embed(
                title=title,
                description=f"{embed_data['user_name']}'s financial status",
                color=EmbedFactory.COLORS['economy'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="Current Balance", value=f"${embed_data['balance']:,}", inline=True)
            embed.add_field(name="Total Earned", value=f"${embed_data['total_earned']:,}", inline=True)
            embed.add_field(name="Total Spent", value=f"${embed_data['total_spent']:,}", inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            main_file = discord.File("./assets/main.png", filename="main.png")
            embed.set_thumbnail(url="attachment://main.png")

            return embed, main_file

        except Exception as e:
            logger.error(f"Error building economy balance embed: {e}")
            return await EmbedFactory.build_error_embed("Economy balance embed error")

    @staticmethod
    async def build_economy_work_embed(embed_data: dict) -> tuple[discord.Embed, discord.File]:
        """Build economy work embed"""
        try:
            embed = discord.Embed(
                title="Mission Completed",
                description=embed_data['scenario'],
                color=EmbedFactory.COLORS['success'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="Compensation", value=f"+${embed_data['earnings']:,}", inline=True)
            embed.add_field(name="Next Assignment", value="Available in 1 hour", inline=True)

            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            main_file = discord.File("./assets/main.png", filename="main.png")
            embed.set_thumbnail(url="attachment://main.png")

            return embed, main_file

        except Exception as e:
            logger.error(f"Error building economy work embed: {e}")
            return await EmbedFactory.build_error_embed("Economy work embed error")

    @staticmethod
    async def build_error_embed(error_message: str) -> tuple[discord.Embed, discord.File]:
        """Build error embed with main.png thumbnail"""
        try:
            embed = discord.Embed(
                title="System Error",
                description=f"Critical system malfunction detected: {error_message}",
                color=EmbedFactory.COLORS['error'],
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(name="Status", value="Operation Failed", inline=True)
            embed.add_field(name="Action Required", value="System diagnostic needed", inline=True)
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")

            # Always use main.png for errors
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

            threat_levels = ["Low", "Medium", "High", "Critical"]
            threat_level = threat_levels[min(level-1, 3)] if level > 0 else "Unknown"
            embed.add_field(name="Threat Level", value=f"Class {level} - {threat_level}", inline=True)
            embed.add_field(name="Status", value=state.replace('_', ' ').title(), inline=True)

            if respawn_time:
                embed.add_field(name="Respawn", value=f"{respawn_time}s", inline=True)

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