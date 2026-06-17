# Pokémon BW AP QoL Plugin

Changelog

## v15
* Updated the code to work with v0.3.31 of the main APworld @Slimey
* Fixed a conflict between `blind_trainers` and `faster_story`
* Added two new YAML options: `intro_skip` and `intro_skip_gender` @Slimey
  * `intro_skip` skips the Prof Juniper introduction at the beginning of the game. The trainer name will match the name setr in the YAML (or the 7 first characters if longer)
  * `intro_skip_gender` sets the gender that will be chosen if intro_skip is on

## v14
* Added 3 new YAML options: `blind_trainers`, `guaranteed_catch` and `remove_dust_cloud_items`
  * `blind_trainers` sets trainers' sight to 0 so they don't notice the player
  * `guaranteed_catch` makes all Poké Ball guaranteed to succeed on wild Pokémon
  * `remove_dust_cloud_items` makes dust clouds give encounters every time

## v13
* Initial GitHub release 
* Rewrote and cleaned the entire init file to optimize loading times and make more YAML options
  * `instant_text`,  `faster_story`, `remove_pickup_animation`, `gym_warps` and `hm_use` now need to be set in the BW YAML
  * Delete 4, the Repel re-use prompt and the shortcut/skip prompts will always be applied by the plugin regardless of the options
* Added a new YAML option: `guaranteed_fishing`
  * The Super Rod will always land on a Pokémon, but reeling in time is still necessary to get the encounter

## v12
* Added a Repel re-use prompt (all credit goes to @ OnlySpaghettiCode)
* Added two new YAML options: `bike_everywhere` and `remove_surf_bike_music`
  * `bike_everywhere` allows the Bicycle to be used nearly everywhere, including inside buildings
  * `remove_surf_bike_music` prevents the BGM to change when surfing or biking

## v11
* Removed the fanfare skips in the Player's Room to fully fix compatibility with the Starter Rando plugin

## v10
* Pokémon League and N's Castle
  * Prevented a softlock when going back to N's Castle 1F after using the Delete 4 NPC
  * Added a trigger to stop the player going back to the Champion's Room from N's Castle 1F
  * Adjusted some flags to prevent visual issues when fighting Alder in the Champion's Room after using Delete 4
* Nuvema Town
  * Adjusted the script of the Player's Room to fix compatibility with the Starter Rando plugin
* Field Moves
  * Cut, Strength, Waterfall and Dive do not require teaching anymore to be used
  * Removed the confirmation window before using a field move
  * ???
* Added an Easter Egg somewhere in Unova

## v9
* Striaton City
  * Changed the walk animations to fast walk
* Route 3 and Wellspring Cave
  * Removed the mandatory double battle against the twins. Talking to them will initiate the fight if you have at least two Pokémon
  * Moved the Cheren fight closer to Wellspring Cave, making it possible to go to Nacrene City before triggering it
  * Removed the trigger that forces the player to finish the Wellspring Cave event before going to Nacrene City
  * Removed the cutscene where Cheren explains how dark grass work. A permanent NPC takes his place and can be talked to to get the explanation
  * Changed the walk animations to fast walk
* Nacrene City and Museum
  * Made the fight against N unskippable. Without the plugin, the fight can be missed if you complete Pinwheel Forest before entering Nacrene Museum
  * Adjusted multiple flags to avoid characters like Lenora being on 2 different places on the map at the same time
  * Changed the walk animations to fast walk
* Pinwheel Forest
  * Removed the trigger that forces the player to clear Pinwheel Forest before going to the Dragon Skull check. Without the plugin, it is only doable before clearing Nacrene Gym
  * Fixed invisible Burgh in the last cutscene if you fight team Plasma before clearing Nacrene Gym
  * Fixed the BGM being stuck to the team Plasma event if you clear Nacrene Gym after Pinwheel Forest
  * Changed the walk animations to fast walk

## v8
* Fixed the Pokémon League Center Plasma grunt NPC not teleporting in front of the Throne Room

## v7
* Adjusted Delete 4
  * Made the Plasma grunt in the Pokémon League Center teleport the player in front of the Throne Room instead of N's Castle 3F
  * Added a Plasma grunt NPC in front of the Throne Room to warp back to the Pokémon League Center
  * Adjusted the dialogs of the NPC guarding the Elite Four Entrance to mention the Delete 4 Plasma grunt NPC
  * Talking to Ghetsis before entering the Throne Room is now optional
  * Added a dialog prompt to skip the Throne Room cutscenes and fight the Legendary right away
  * Catching the Legendary is not required anymore to progress the story
  * Adding the Legendary to the party will not put it in first place anymore
  * Changed the walk animations to fast walk
* Adjusted some events at the beginning of the game
  * Mom will now give the Town Map and the Running Shoes just after the XTransceiver
  * Removed the Mom cutscene after obtaining the Pokédex
  * Removed the Mom cutscene on Route 2
  * Adjusted the cutscene in Juniper Lab to make Cheren and Bianca leave before the player

## v6
* Fixed a texture issue in Mistralton Gym
* Fixed invisible Cheren on Route 4

## v5
* Fixed an issue with fanfare skips that prevented some BGM changes (like the Follow Me music getting stuck in Nacrene City)
  * A small delay has been added to some item pickups because of that
* Shortened Nuvema Town to Route 2 events
  * Adjusted some of the dialogs
  * Removed the cutscene in Bianca's house
  * Removed the cutscene at the end of Route 1 and the XTransceiver call
  * Removed the Accumula Pokémon Center cutscene
  * Removed the XTransceiver call on Route 2
  * Made Prof Juniper skip the catch tutorial and go back to Nuvema Town
  * Cut some animations and dialogs in the Ghetsis cutscene of Accumula Town
  * Changed the walk animations to fast walk

## v4
* Added optional gym warps to make gyms faster
  * Taking the warps in Striaton Gym and Nacrene Gym will solve their puzzles
* Removed the badge case cutscenes normally playing after defeating a Gym Leader
* Added a dialog prompt to take a shortcut for Skyarrow Bridge
* Shortened the Burgh events in Castelia City
  * Removed the sequence on Prime Pier
  * Changed the walk animations to fast walk
* Shortened the Bianca events in Nimbasa City
  * Changed the walk animations to fast walk
  * Removed the trigger forcing the player to follow Bianca when attempting to go to Route 5 before visiting the Musical Theater
  * Removed the Dress up tutorial and adjusted the dialog for it
  * Removed the cutscene with Bianca's dad after going to the Musical Theater
* Shortened N's event in Nimbasa City East
  * Changed the walk animations to fast walk
  * Removed the 3D ferry wheel cutscene
* Shortened the events on Route 5 after defeating Elesa
  * Changed the walk animations to fast walk
  * Removed the 3D bridge cutscene and adjusted the dialog for it

## v3
* Added Instant Text
  * Fixed the freeze when mashing buttons at the start of a trainer battle from the QoL script
  * Fixed the empty text boxes issues from the QoL script
* Added Delete 4
  * The Plasma Grunt in Pokémon League Center can teleport the player in N's Castle as soon as you reach Pokémon League

## v2
* Switched to OTPP patches

## v1
* Removes HM cut-ins
* Removes item pickup animations and enables skippable fanfare
* Removes the catching tutorial on Route 1
