# Pokémon BW QoL APworld Plugin
*An optional APworld that adds some QoL features to the main BW APworld (requires v0.3.29 or later)*

## Features
- Adds a Repel re-use prompt @OnlySpaghettiCode
- Makes the Plasma grunt who teleports the player to N's Castle available at all time, allowing the player to skip the Elite 4
- Adds prompts to skip Skyarrow Bridge and N's Castle cutscenes
- Adds `instant_text` as a YAML option:
  - If set to `true`, the in-game text will appear instantly.
- Adds `faster_story` as a YAML option:
  - If set to `true`, some story events will be changed to become more time efficient or to add more routing options;
  - Check the [changelog.md](https://github.com/Radis7Noir/pokemon_bw_qol_plugin/blob/main/changelog.md) file to see the changes.
- Adds `remove_pickup_animation` as a YAML option:
  - If set to `true`, the item pickup animation will be removed, and most of the fanfare sounds will become skippable.
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

## Instructions
- Download the latest release of the plugin APworld
- Place it in the `custom_worlds` folder of the Archipelago folder
- Restart the AP launcher
- Add the following options to the Black and White YAML under `plugin_options`:
```
plugin_options:
    qol:
      instant_text: true
      faster_story: true
      remove_pickup_animation: true # also makes most fanfares skippable
      gym_warps: true
      hm_use: fastest # currently only supports fastest
      guaranteed_fishing: true # 
      bike_everywhere: true
      remove_surf_bike_music: true
```
- Change the above options as seen fit and generate the seed as usual
  - When running the .apwhite/.apblack patch, the produced .nds file should include the features that have been activated.
- To update mid-run, install the plugin apworld, delete the patched ROM and run the patch file again
  - Updating mid-run will only apply the options that were activated in the YAML used for generation;
  - A ready to use apworld that includes all features activated by default will be included in the releases. Use it to update mid-run when a feature you want was not set in your YAML.
