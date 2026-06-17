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

    # The following fields need to always be set by the plugin creator.
    # "domain" is the key that is used for plugin options and settings, i.e. the player needs to put
    # >  plugin_options:
    # >    <domain>:
    # >      option_1: 123
    # into their player yaml and
    # >  plugin_settings:
    # >    <domain>:
    # >      setting_1: 123
    # into their host.yaml.
    # The version needs to always have the semantic format, i.e. "<major>.<minor>.<patch>".
    name = "Pokemon BW QoL Plugin"
    domain = "qol"
    version = "1.15.0"
    author = "RadisNoir"

    # This is called during the patching process, after the main apworld did all its standard modifications to the rom.
    def patch(self):
        if DEV: return  # This line is only relevant to the main apworld dev and can be removed if you want.

        # Proposal:
        # You change all (or at least most) options if you want to settings, i.e. the user needs to define those in
        # their host.yaml instead of the player yaml. To do that, just change the "self.get_option(..." to
        # "self.get_setting(..." for all options you want to convert.
        # However, I haven't tested yet whether the settings in the host.yaml actually work.


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
            for i in [82, 349, 353, 361, 428, 429, 435, 436]:
                loaded_file = pkgutil.get_data(__name__, f"files/a003/a003_{i:03d}")
                narc_file = self.get_from_narc("a/0/0/3", i)
                self.otpp_patch_array(narc_file, loaded_file)

            for i in [12, 14, 18, 20, 32, 34, 36, 38, 58, 62, 124, 126, 128, 154, 194, 216, 228, 242, 308, 310,
                      634, 638, 642, 648, 658, 778, 780, 782, 792, 794]:
                loaded_file = pkgutil.get_data(__name__, f"files/a057/a057_{i:03d}")
                narc_file = self.get_from_narc("a/0/5/7", i)
                self.otpp_patch_array(narc_file, loaded_file)

            for i in [16, 28, 62, 154, 155, 321]:
                loaded_file = pkgutil.get_data(__name__, f"files/a125/a125_{i:03d}")
                narc_file = self.get_from_narc("a/1/2/5", i)
                self.otpp_patch_array(narc_file, loaded_file)

# Blind Trainers
        if option_or_setting("blind_trainers", False):
            faster_story = option_or_setting("faster_story", False)
            for i in [7, 18, 29, 45, 46, 63, 97, 108, 114, 121, 152, 153, 154, 155, 158, 160, 161, 162, 163, 164,
                      191, 192, 195, 196, 197, 198, 199, 200, 201, 202, 206, 210, 216, 217, 218, 221, 223, 226, 227,
                      235, 236, 238, 240, 255, 317, 319, 321, 325, 326, 329, 331, 333, 337, 339, 340, 341, 345, 346,
                      348, 352, 353, 354, 355, 365, 368, 370, 374, 376, 378, 383, 387, 423]:
                if faster_story and i in [154, 155]:
                    loaded_file = pkgutil.get_data(__name__, f"files/a125/blind_trainers/faster_story/{i:03d}")
                else:
                    loaded_file = pkgutil.get_data(__name__, f"files/a125/blind_trainers/{i:03d}")
                narc_file = self.get_from_narc("a/1/2/5", i)
                self.otpp_patch_array(narc_file, loaded_file)

# Guaranteed Catch
        if option_or_setting("guaranteed_catch", False):
            ov_93 = self.get_overlay(93)
            ov_93[0x15B82:0x15B84] = b'\x00\x00'

# Remove Phenomenon Items
        if option_or_setting("remove_dust_cloud_items", False):
            ov_21 = self.get_overlay(21)
            ov_21[0x22adc] = 0xb5

# Field Moves
        match option_or_setting("hm_use", False):
            case "fast":
                suffix = "fast"
            case "fastest":
                suffix = "fastest"
            case _:
                suffix = "rock_smash"
        loaded_file = pkgutil.get_data(__name__, f"files/a003/a003_280_{suffix}")
        narc_file = self.get_from_narc("a/0/0/3", 280)
        self.otpp_patch_array(narc_file, loaded_file)
        loaded_file = pkgutil.get_data(__name__, f"files/a057/a057_867_{suffix}")
        narc_file = self.get_from_narc("a/0/5/7", 867)
        self.otpp_patch_array(narc_file, loaded_file)

# Guaranteed Fishing
        if option_or_setting("guaranteed_fishing", False):
            for i in [0, 1, 2, 6, 49, 53, 58, 69, 71, 72, 73, 75, 77, 79, 80, 81, 82, 84, 93, 94, 98,
                      101, 103, 104, 105, 108, 109, 110, 111]:
                loaded_file = pkgutil.get_data(__name__, f"files/a126/a126_{i:03d}")
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
                loaded_file = pkgutil.get_data(__name__, f"files/a008/a008_{i:03d}")
                narc_file = self.get_from_narc("a/0/0/8", i)
                self.otpp_patch_array(narc_file, loaded_file)

            for i in [7, 18, 19, 29, 63, 97, 98, 108, 114, 121]:
                loaded_file = pkgutil.get_data(__name__, f"files/a125/a125_{i:03d}")
                narc_file = self.get_from_narc("a/1/2/5", i)
                self.otpp_patch_array(narc_file, loaded_file)

# No Pickup Animation & Fanfare Skip
        if option_or_setting("remove_pickup_animation", False):
            for i in [862, 864]:
                loaded_file = pkgutil.get_data(__name__, f"files/a057/a057_{i:03d}")
                narc_file = self.get_from_narc("a/0/5/7", i)
                self.otpp_patch_array(narc_file, loaded_file)

# Always On (Repel Prompt, Shortcuts, Delete 4)
        for i in [82, 141, 263, 267, 268, 300]:
            loaded_file = pkgutil.get_data(__name__, f"files/a003/a003_{i:03d}")
            narc_file = self.get_from_narc("a/0/0/3", i)
            self.otpp_patch_array(narc_file, loaded_file)

        for i in [272, 292, 502, 504, 528, 554, 556, 872]:
            loaded_file = pkgutil.get_data(__name__, f"files/a057/a057_{i:03d}")
            narc_file = self.get_from_narc("a/0/5/7", i)
            self.otpp_patch_array(narc_file, loaded_file)

        for i in [251, 252, 264, 277]:
            loaded_file = pkgutil.get_data(__name__, f"files/a125/a125_{i:03d}")
            narc_file = self.get_from_narc("a/1/2/5", i)
            self.otpp_patch_array(narc_file, loaded_file)


# Just run this python script and it will pack this plugin into an apworld file for you.
# Note that any file or folder that contains "_temp" in its name will be ignored and the archipelago.json that's
# bundled will be overwritten.
if __name__ == '__main__':
    from data.build import build

    build(Plugin.name, Plugin.version, Plugin.author)
