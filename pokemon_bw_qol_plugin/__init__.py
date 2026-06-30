# Do not change anything about the imports unless you know what you do
import pkgutil
from typing import TYPE_CHECKING
if __name__ == '__main__':
    from data.api import PluginProtocol
else:
    from .data.api import PluginProtocol
try:
    if TYPE_CHECKING:
        from worlds.pokemon_bw.ndspy.rom import NintendoDSRom
        from worlds.pokemon_bw.rom import PokemonBWPatch
        from worlds.pokemon_bw.items import PokemonBWItem
        from worlds.pokemon_bw.data import SpeciesData, ExtendedRule
        from worlds.pokemon_bw import PokemonBWWorld
    from worlds.pokemon_bw.plugins._dev import DEV
except ImportError:
    DEV = False


# This has to exactly be named "Plugin" and should inherit from "PluginProtocol"
class Plugin(PluginProtocol):

    name = "Pokemon BW QoL Plugin"
    domain = "qol"
    version = "1.17.0"
    author = "RadisNoir"

    # This is called during the patching process, after the main apworld did all its standard modifications to the rom.
    def patch(self):
        if DEV: return  # This line is only relevant to the main apworld dev and can be removed if you want.

        option_or_setting = self.get_option if self.domain in self.all_plugin_options else self.get_setting

# Instant Text
        if option_or_setting("instant_text", False):
            arm9 = self.get_arm9()
            if self._rom.name[:9] == b'POKEMON\x20W':
                arm9[0x18fda:0x18fe0] = b'\x00\x28\xc0\x46\xc0\x46'
                arm9[0x19090:0x19098] = b'\x00\x48\x00\x47\x39\x05\x0a\x02'
                extra_code = pkgutil.get_data(__name__, "files/w_insta_text_append.bin")
                arm9[0x9c538:0x9c538+len(extra_code)] = extra_code
            else:
                arm9[0x18fc0:0x18fc4] = b'\xc0\x46\xc0\x46'
                arm9[0x19074:0x1907c] = b'\x00\x48\x00\x47\x21\x05\x0a\x02'
                extra_code = pkgutil.get_data(__name__, "files/b_insta_text_append.bin")
                arm9[0x9c520:0x9c520+len(extra_code)] = extra_code

#Battle Scene
        match option_or_setting("battle_scene", False):
            case "turned_on":
                pass
            case "turned_off":
                arm9 = self.get_arm9()
                arm9[0x0434e] = 0x0a
            case _:
                pass

#Battle Style
        match option_or_setting("battle_style", False):
            case "shift":
                pass
            case "set":
                arm9 = self.get_arm9()
                arm9[0x04346] = 0x0a
            case _:
                pass

#Intro Skip
        if option_or_setting("skip_intro", False):
            name = self.patch_instance.player_name[:7]  # Player name from the yaml
            output = bytearray()
            from_int = lambda num: num.to_bytes(2, byteorder="little")
            output += b'\xa1\x6a'
            output += (b'\x01\x22' 
                       if option_or_setting("skip_intro_gender", "male").casefold() == "female" 
                       else b'\x00\x22')
            output += b'\x60\x6d\x09\x6a'
            output += from_int(0x2400 + len(name))
            output += b'\x8c\x70'
            for i in range(len(name)):
                enc = name[i].encode()
                output += from_int(0x2400 + enc[0])
                output += from_int(0x700c + 0x40 * (i*2 + 8))
                output += from_int(0x2400 + (enc[1] if len(enc) > 1 else 0))
                output += from_int(0x700c + 0x40 * (i*2 + 9))
            output += b'\xff\x24'
            output += from_int(0x700c + 0x40 * (len(name) * 2 + 8))
            output += from_int(0x700c + 0x40 * (len(name) * 2 + 9))
            addr = (0x021bc4f8, 0x21b95c0, 0x2cc8) if self._rom.name[:9] == b'POKEMON\x20W' else (0x021bc4a4, 0x21b95a0, 0x2c94)
            offset = (addr[0] - (addr[1] + addr[2] + len(output) + 4)) & 0x7FFFFF
            output += from_int(((offset >> 12) & 0x07FF) | 0xF000) + from_int(((offset >> 1) & 0x07FF) | 0xF800)
            output += b'\x01\x20\x38\xbd'
            ov_88 = self.get_overlay(88)
            ov_88[addr[2]:addr[2]+len(output)] = output

# Faster Story
        if option_or_setting("faster_story", False):
            for i in [349, 361, 428, 429, 435]:
                loaded_file = pkgutil.get_data(__name__, f"files/a003/faster_story/{i:03d}")
                narc_file = self.get_from_narc("a/0/0/3", i)
                self.otpp_patch_array(narc_file, loaded_file)

            for i in [18, 20, 34, 38, 58, 62, 126, 128, 154, 194, 216, 228, 242,
                      634, 638, 658, 778, 780, 782, 792, 794]:
                loaded_file = pkgutil.get_data(__name__, f"files/a057/faster_story/{i:03d}")
                narc_file = self.get_from_narc("a/0/5/7", i)
                self.otpp_patch_array(narc_file, loaded_file)

            for i in [28]:
                loaded_file = pkgutil.get_data(__name__, f"files/a125/faster_story/{i:03d}")
                narc_file = self.get_from_narc("a/1/2/5", i)
                self.otpp_patch_array(narc_file, loaded_file)

# Pokemon Entrance Animations
        match option_or_setting("pokemon_entrance_animations", False):
            case "disable_always":
                ov_93 = self.get_overlay(93)
                ov_93[0x3733b] = 0xe0
                for i in (0x368c8, # my poke solo 2
                          0x3671e, # my poke single 2
                          0x361ac, # opp poke single 2
                          0x35b98, 0x35c16, # wild double 5, 6
                          0x35964, # trainer single 5, 8
                          0x35686, 0x356ca):# wild single 4, 5
                    ov_93[i:i+4] = b'\0\0\0\0'
            case "disable_on_switch_and_wilds":
                ov_93 = self.get_overlay(93)
                ov_93[0x3733b] = 0xe0
                for i in (0x3671e, # my poke single 2
                          0x361ac, # opp poke single 2
                          0x35b98, 0x35c16, # wild double 5, 6
                          0x35686, 0x356ca):# wild single 4, 5
                    ov_93[i:i+4] = b'\0\0\0\0'
            case "disable_on_switch":
                ov_93 = self.get_overlay(93)
                ov_93[0x3733b] = 0xe0
            case "vanilla":
                pass
            case _:
                pass

# Blind Trainers
        if option_or_setting("blind_trainers", False):
            ov_21 = self.get_overlay(21)
            ov_21[0x2635e:0x26360] = b'\x09\xe0'

# Guaranteed Catch
        if option_or_setting("guaranteed_catch", False):
            ov_93 = self.get_overlay(93)
            ov_93[0x15B82:0x15B84] = b'\x00\x00'

# Remove Phenomenon Items
        if option_or_setting("remove_dust_cloud_items", False):
            ov_21 = self.get_overlay(21)
            ov_21[0x22adc] = 0xb5

# TMs/HMs Fully Compatible
        if option_or_setting("tmhm_fully_compatible", False):
            for i in range(1, 668):
                if i == 151:
                    continue
                loaded_file = pkgutil.get_data(__name__, f"files/a016/tmhm_fully_compatible/{i:03d}")
                narc_file = self.get_from_narc("a/0/1/6", i)
                self.otpp_patch_array(narc_file, loaded_file)

# Fast Egg Hatch
        if option_or_setting("fast_hatch", False):
            for i in range(1, 668):
                narc_file = self.get_from_narc("a/0/1/6", i)
                narc_file[0x13] = 0x01

# Field Moves
        if self.all_plugin_options.get("extra_logic", {}).get("hm_with_badges", False):
            match option_or_setting("hm_use", False):
                case "fast":
                    suffix = "badgefast"
                case "fastest":
                    suffix = "badgefast"
                case "vanilla":
                    suffix = "badgevanilla"
                case _:
                    suffix = "badgevanilla"
            loaded_file = pkgutil.get_data(__name__, f"files/a057/hm_use/867_{suffix}")
            narc_file = self.get_from_narc("a/0/5/7", 867)
            self.otpp_patch_array(narc_file, loaded_file)
        else:
            match option_or_setting("hm_use", False):
                case "fast":
                    suffix = "fast"
                case "fastest":
                    suffix = "fast"
                case "vanilla":
                    suffix = "vanilla"
                case _:
                    suffix = "vanilla"
            loaded_file = pkgutil.get_data(__name__, f"files/a057/hm_use/867_{suffix}")
            narc_file = self.get_from_narc("a/0/5/7", 867)
            self.otpp_patch_array(narc_file, loaded_file)

# Guaranteed Fishing
        if option_or_setting("guaranteed_fishing", False):
            for i in [0, 1, 2, 6, 49, 53, 58, 69, 71, 72, 73, 75, 77, 79, 80, 81, 82, 84, 93, 94, 98,
                      101, 103, 104, 105, 108, 109, 110, 111]:
                loaded_file = pkgutil.get_data(__name__, f"files/a126/guaranteed_fishing/{i:03d}")
                narc_file = self.get_from_narc("a/1/2/6", i)
                self.otpp_patch_array(narc_file, loaded_file)

# Bike Everywhere / Remove Surf & Bike Music
        bike_everywhere = option_or_setting("bike_everywhere", False)
        remove_surf_bike_music = option_or_setting("remove_surf_bike_music", False)
        if bike_everywhere:
            loaded_file = pkgutil.get_data(__name__, "files/a012/a012_000_bike")
            narc_file = self.get_from_narc("a/0/1/2", 0)
            self.otpp_patch_array(narc_file, loaded_file)
        if remove_surf_bike_music:
            loaded_file = pkgutil.get_data(__name__, "files/a012/a012_000_music")
            narc_file = self.get_from_narc("a/0/1/2", 0)
            self.otpp_patch_array(narc_file, loaded_file)

# Gym Warps
        if option_or_setting("gym_warps", False):
            for i in [515, 518, 519, 520, 524, 525, 527, 538, 548, 552, 564, 565, 595, 606, 615]:
                loaded_file = pkgutil.get_data(__name__, f"files/a008/gym_warps/{i:03d}")
                narc_file = self.get_from_narc("a/0/0/8", i)
                self.otpp_patch_array(narc_file, loaded_file)

            for i in [7, 18, 19, 29, 63, 97, 98, 108, 114, 121]:
                loaded_file = pkgutil.get_data(__name__, f"files/a125/gym_warps/{i:03d}")
                narc_file = self.get_from_narc("a/1/2/5", i)
                self.otpp_patch_array(narc_file, loaded_file)

# No Pickup Animation & Fanfare Skip
        if option_or_setting("remove_pickup_animation", False):
            for i in [862, 864]:
                loaded_file = pkgutil.get_data(__name__, f"files/a057/remove_pickup_animation/{i:03d}")
                narc_file = self.get_from_narc("a/0/5/7", i)
                self.otpp_patch_array(narc_file, loaded_file)

# Always On (Repel Prompt, Shortcuts, Delete 4, Fast Text, Field Move Text)
        for i in [21, 67, 141, 263, 267, 268, 280, 300, 353, 356, 385]:
            loaded_file = pkgutil.get_data(__name__, f"files/a003/{i:03d}")
            narc_file = self.get_from_narc("a/0/0/3", i)
            self.otpp_patch_array(narc_file, loaded_file)

        for i in [12, 14, 32, 36, 124, 272, 292, 308, 310, 502, 504, 528, 554, 556, 642, 648, 652, 866, 706, 872]:
            loaded_file = pkgutil.get_data(__name__, f"files/a057/{i:03d}")
            narc_file = self.get_from_narc("a/0/5/7", i)
            self.otpp_patch_array(narc_file, loaded_file)

        for i in [16, 62, 154, 155, 251, 252, 264, 277, 321]:
            loaded_file = pkgutil.get_data(__name__, f"files/a125/{i:03d}")
            narc_file = self.get_from_narc("a/1/2/5", i)
            self.otpp_patch_array(narc_file, loaded_file)

        #Text Speed Fast + Forgettable HMs
        arm9 = self.get_arm9()
        arm9[0x04332] = 0x02
        if self._rom.name[:9] == b'POKEMON\x20W':
            arm9[0x00fc4:0x00fc6] = b'\xe8\x3d'
            arm9[0x1d300:0x1d304] = b'\x00\x20\x70\x47'
        else:
            arm9[0x00fc4:0x00fc6] = b'\xf4\x3d'
            arm9[0x1d2e4:0x1d2e8] = b'\x00\x20\x70\x47'

# Just run this python script and it will pack this plugin into an apworld file for you.
# Note that any file or folder that contains "_temp" in its name will be ignored and the archipelago.json that's
# bundled will be overwritten.
if __name__ == '__main__':
    from data.build import build

    build(Plugin.name, Plugin.version, Plugin.author)
