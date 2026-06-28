# Pokémon BW QoL APworld Plugin
An optional APworld that adds some QoL features to the main BW APworld

The latest version of the main APworld (0.3.34) is only compatible with v16 or later of the plugin.

## Features
- Adds a Repel re-use prompt @OnlySpaghettiCode
- Makes the Plasma grunt who teleports the player to N's Castle available at all time, allowing the player to skip the Elite 4
- Adds prompts to skip Skyarrow Bridge and N's Castle cutscenes
- Moves can be taught over HMs
- `instant_text` makes the in-game text appear instantly
- `intro_skip` skips the Prof Juniper introduction at the beginning of the game and use the YAML name as the player's name
- `intro_skip_gender` set the player's gender when `intro_skip` in on
- `faster_story` changes some story events to make them more time efficient
  - Check the [changelog.md](https://github.com/Radis7Noir/pokemon_bw_qol_plugin/blob/main/changelog.md) file to see the changes
- `blind_trainers` makes the trainers not notice the player
- `guaranteed_catch` makes any kind of Poké Ball guaranteed to catch a wild Pokémon
- `remove_pickup_animation` removes the item pickup animation and makes most of the fanfare sounds skippable
- `remove_dust_cloud_items` makes dust clouds phenomena only give encounters (flying shadows can still give items)
- `gym_warps` adds a warp pad to every gym to skip their puzzles
- `hm_use` sets the behavior of field moves:
  - `vanilla` does not change anything
  - `fastest` skips the confirmation window and the cut-in animation. Cut, Strength, Waterfall and Dive also become usable without teaching
- `guaranteed_fishing` makes the Super Rod always land on a Pokémon, but reeling in time is still necessary to get the encounter
- `bike_everywhere` makes the Bicycle usable almost everywhere, including inside buildings
- `remove_surf_bike_music` prevent the BGM to change when surfing or biking.
- `battle_scene` turns off the battle animations or leaves them on
- `battle_style` turns off the switch prompt after defeating a trainer's pokemon or leaves it on
- `pokemon_entrance_animations` can disable the ball throwing animations when sending a pokémon @Slimey
  - `vanilla` does not change anything
  - `only_on_switch` will only remove the animations when the player or the opponent sends another pokemon
  - `disable_on_switch_and_wilds` will additionally remove the player's lead entrance animation against wilds
  - `disable_always` will additionally remove the player's lead entrance animation against trainers (except in triple, rotation and tag battles)
- `tmhm_fully_compatible` makes tms and hms learnable by all pokemon
- `fast_hatch` makes all eggs hatch in one cycle

## Instructions
- Download the latest release of the plugin APworld
- Place it in the `custom_worlds` folder of the Archipelago folder
- Restart the AP launcher
- Add the following options to the Black and White YAML under `plugin_options`:
```
  plugin_options:
    qol:
      skip_intro: true
      skip_intro_gender:
        male: 50
        female: 50
      instant_text: true
      faster_story: true
      gym_warps: true
      blind_trainers: true
      guaranteed_catch: true
      hm_use: fastest
      tmhm_fully_compatible: true
      remove_pickup_animation: true  # also makes most fanfares skippable
      bike_everywhere: true
      guaranteed_fishing: true  # reeling in time is still necessary
      remove_dust_cloud_items: true
      remove_surf_bike_music: true
      battle_scene: turned_off
      battle_style: set
      pokemon_entrance_animations:
        vanilla: 0
        disable_on_switch: 0  # disables switching animations
        disable_on_switch_and_wilds: 50  # additionally removes the player's lead animation against wilds
        disable_always: 0  # additionally removes the player's lead animation against most trainers
      fast_hatch: true
```
- Change the above options as seen fit and generate the seed as usual
  - When running the .apwhite/.apblack patch, the produced .nds file should include the features that have been activated.
