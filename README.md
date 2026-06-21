# Pokémon BW QoL APworld Plugin
*An optional APworld that adds some QoL features to the main BW APworld (requires v0.3.29 or later)*

## Features
- Adds a Repel re-use prompt @OnlySpaghettiCode
- Makes the Plasma grunt who teleports the player to N's Castle available at all time, allowing the player to skip the Elite 4
- Adds prompts to skip Skyarrow Bridge and N's Castle cutscenes
- Adds `instant_text` as a YAML option:
  - If set to `true`, the in-game text will appear instantly.
- Adds `intro_skip` as a YAML option:
  - If `intro_skip` is set to `true`, the gender of the trainer will be set by this option.
- Adds `intro_skip_gender` as a YAML option:
  - If set to `true`, the Prof Juniper introduction at the beggining of the game will be skipped.
- Adds `faster_story` as a YAML option:
  - If set to `true`, some story events will be changed to become more time efficient or to add more routing options;
  - Check the [changelog.md](https://github.com/Radis7Noir/pokemon_bw_qol_plugin/blob/main/changelog.md) file to see the changes.
 - Adds `blind_trainers` as a YAML option:
  - If set to `true`, trainers won't notice you unless spoken to.
 - Adds `guaranteed_catch` as a YAML option:
  - If set to `true`, any Poké Ball will be guaranteed to catch a wild Pokémon.
- Adds `remove_pickup_animation` as a YAML option:
  - If set to `true`, the item pickup animation will be removed, and most of the fanfare sounds will become skippable.
- Adds `remove_dust_cloud_items` as a YAML option:
  - If set to `true`, dust clouds will only give encounters. Flying shadows can still give items.
- Adds `gym_warps` as a YAML option:
  - If set to `true`, warps will be added to every gym to make it possible to skip their puzzles.
- Adds `hm_use` as a YAML option:
  - If set to `vanilla`, HMs will work as they do in the vanilla games;
  - If set to `fast`, the HM cut-in animations will be skipped and Cut, Strength, Waterfall and Dive become usable without teaching;
  - If set to `fastest`, all `fast` changes will be included and the confirmation windows will be skipped;
  - Only `fastest` is supported for now.
- Adds `guaranteed_fishing` as a YAML option:
  - If set to `true`, the Super Rod will always land on a Pokémon. Reeling in time is still necessary to get the encounter.
- Adds `bike_everywhere` as a YAML option:
  - If set to `true`, the Bicycle becomes usable almost everywhere, including inside buildings.
- Adds `remove_surf_bike_music` as a YAML option:
  - If set to `true`, the BGM will not change anymore when surfing or biking.
- `battle_scene` turns off the battle animations or leaves them on
- `battle_style` turns off the switch prompt after defeating a trainer's pokemon or leaves it on
- `pokemon_entrance_animations` can disable the ball throwing animations when sending a pokémon @Slimey
  - `vanilla` does not change anything
  - `only_on_switch` will only remove the animations when the player or the opponent sends another pokemon
  - `disable_on_switch_and_wilds` will additionally remove the player's lead entrance animation against wilds
  - `disable_always` will additionally remove the player's lead entrance animation against trainers (except in triple, rotation and tag battles)
- `tmhm_fully_compatible` makes tms and hms learnable by all pokemon
- `forgettable_hms` allows any move to be taught over an hm move
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
      battle_scene: turned_off
      battle_style: set
      pokemon_entrance_animations:
        vanilla: 0
        disable_on_switch: 0  # disables switching animations
        disable_on_switch_and_wilds: 0  # additionally removes the player's lead animation against wilds
        disable_always: 50  # additionally removes the player's lead animation against most trainers
      guaranteed_catch: true
      faster_story: true
      blind_trainers: true
      remove_pickup_animation: true  # also makes most fanfares skippable
      gym_warps: true
      hm_use: fastest  # currently only supports fastest
      tmhm_fully_compatible: true
      forgettable_hms: true
      guaranteed_fishing: true  # reeling in time is still necessary
      remove_dust_cloud_items: true
      fast_hatch: true
      bike_everywhere: true
      remove_surf_bike_music: true
```
- Change the above options as seen fit and generate the seed as usual
  - When running the .apwhite/.apblack patch, the produced .nds file should include the features that have been activated.
