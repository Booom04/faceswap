#!/usr/bin/env python3
""" Command Line Arguments for tools """
import gettext

from lib.cli.args import FaceSwapArgs
from lib.cli.actions import DirFullPaths, SaveFileFullPaths, Radio, Slider


# LOCALES
_LANG = gettext.translation("tools.sort.cli", localedir="locales", fallback=True)
_ = _LANG.gettext


_HELPTEXT = _("This command lets you sort images using various methods.")


class SortArgs(FaceSwapArgs):
    """ Class to parse the command line arguments for sort tool """

    @staticmethod
    def get_info():
        """ Return command information """
        return _("Sort faces using a number of different techniques")

    @staticmethod
    def get_argument_list():
        """ Put the arguments in a list so that they are accessible from both argparse and gui """
        argument_list = list()
        argument_list.append(dict(
            opts=('-i', '--input'),
            action=DirFullPaths,
            dest="input_dir",
            group=_("data"),
            help=_("Input directory of aligned faces."),
            required=True))
        argument_list.append(dict(
            opts=('-o', '--output'),
            action=DirFullPaths,
            dest="output_dir",
            group=_("data"),
            help=_("Output directory for sorted aligned faces.")))
        argument_list.append(dict(
            opts=("-B", "--batch-mode"),
            action="store_true",
            dest="batch_mode",
            default=False,
            group=_("data"),
            help=_("R|If selected then the input_dir should be a parent folder containing "
                   "multiple folders of faces you wish to sort. The faces "
                   "will be output to separate sub-folders in the output_dir if 'rename' has been "
                   "selected")))
        argument_list.append(dict(
            opts=('-s', '--sort-by'),
            action=Radio,
            type=str,
            choices=("blur", "blur-fft", "distance", "face", "face-cnn", "face-cnn-dissim",
                     "face-yaw", "hist", "hist-dissim", "color-gray", "color-luma", "color-green",
                     "color-orange", "size", "black-pixels"),
            dest='sort_method',
            group=_("sort settings"),
            default="face",
            help=_("R|Sort by method. Choose how images are sorted. "
                   "\nL|'blur': Sort faces by blurriness."
                   "\nL|'blur-fft': Sort faces by fft filtered blurriness."
                   "\nL|'distance' Sort faces by the estimated distance of the alignments from an "
                   "'average' face. This can be useful for eliminating misaligned faces."
                   "\nL|'face': Use VGG Face to sort by face similarity. This uses a pairwise "
                   "clustering algorithm to check the distances between 512 features on every "
                   "face in your set and order them appropriately."
                   "\nL|'face-cnn': Sort faces by their landmarks. You can adjust the threshold "
                   "with the '-t' (--ref_threshold) option."
                   "\nL|'face-cnn-dissim': Like 'face-cnn' but sorts by dissimilarity."
                   "\nL|'face-yaw': Sort faces by Yaw (rotation left to right)."
                   "\nL|'hist': Sort faces by their color histogram. You can adjust the threshold "
                   "with the '-t' (--ref_threshold) option."
                   "\nL|'hist-dissim': Like 'hist' but sorts by dissimilarity."
                   "\nL|'color-gray': Sort images by the average intensity of the converted "
                   "grayscale color channel."
                   "\nL|'color-luma': Sort images by the average intensity of the converted Y "
                   "color channel. Bright lighting and oversaturated images will be ranked first."
                   "\nL|'color-green': Sort images by the average intensity of the converted Cg "
                   "color channel. Green images will be ranked first and red images will be last."
                   "\nL|'color-orange': Sort images by the average intensity of the converted Co "
                   "color channel. Orange images will be ranked first and blue images will be "
                   "last."
                   "\nL|'size': Sort images by their size in the original frame. Faces closer to "
                   "the camera and from higher resolution sources will be sorted first, whilst "
                   "faces further from the camera and from lower resolution sources will be "
                   "sorted last."
                   "\nL|'black-pixels': Sort images by their number of black pixels. Useful when "
                   "faces are near borders and a large part of the image is black."
                   "\nDefault: face")))
        argument_list.append(dict(
            opts=('-k', '--keep'),
            action='store_true',
            dest='keep_original',
            default=False,
            group=_("output"),
            help=_("Keeps the original files in the input directory. Be careful when using this "
                   "with rename grouping and no specified output directory as this would keep the "
                   "original and renamed files in the same directory.")))
        argument_list.append(dict(
            opts=('-t', '--ref_threshold'),
            action=Slider,
            min_max=(-1.0, 10.0),
            rounding=2,
            type=float,
            dest='min_threshold',
            group=_("sort settings"),
            default=-1.0,
            help=_("Float value. Minimum threshold to use for grouping comparison with 'face-cnn' "
                   "and 'hist' methods. The lower the value the more discriminating the grouping "
                   "is. Leaving -1.0 will allow the program set the default value automatically. "
                   "For face-cnn 7.2 should be enough, with 4 being very discriminating. For hist "
                   "0.3 should be enough, with 0.2 being very discriminating. Be careful setting "
                   "a value that's too low in a directory with many images, as this could result "
                   "in a lot of directories being created. Defaults: face-cnn 7.2, hist 0.3")))
        argument_list.append(dict(
            opts=('-fp', '--final-process'),
            action=Radio,
            type=str,
            choices=("folders", "rename"),
            dest='final_process',
            default="rename",
            group=_("output"),
            help=_("R|Default: rename."
                   "\nL|'folders': files are sorted using the -s/--sort-by method, then they are "
                   "organized into folders using the -g/--group-by grouping method."
                   "\nL|'rename': files are sorted using the -s/--sort-by then they are "
                   "renamed.")))
        argument_list.append(dict(
            opts=('-g', '--group-by'),
            action=Radio,
            type=str,
            choices=("blur", "blur-fft", "face-cnn", "face-yaw", "hist", "black-pixels"),
            dest='group_method',
            group=_("output"),
            default="hist",
            help=_("Group by method. When -fp/--final-processing by folders choose the how the "
                   "images are grouped after sorting. Default: hist")))
        argument_list.append(dict(
            opts=('-b', '--bins'),
            action=Slider,
            min_max=(1, 100),
            rounding=1,
            type=int,
            dest='num_bins',
            group=_("output"),
            default=5,
            help=_("Integer value. Number of folders that will be used to group by blur, "
                   "face-yaw and black-pixels. For blur folder 0 will be the least blurry, while "
                   "the last folder will be the blurriest. For face-yaw the number of bins is by "
                   "how much 180 degrees is divided. So if you use 18, then each folder will be "
                   "a 10 degree increment. Folder 0 will contain faces looking the most to the "
                   "left whereas the last folder will contain the faces looking the most to the "
                   "right. If the number of images doesn't divide evenly into the number of "
                   "bins, the remaining images get put in the last bin. For black-pixels it "
                   "represents the divider of the percentage of black pixels. For 10, first "
                   "folder will have the faces with 0 to 10%% black pixels, second 11 to 20%%, "
                   "etc. Default value: 5")))
        argument_list.append(dict(
            opts=('-l', '--log-changes'),
            action='store_true',
            group=_("settings"),
            default=False,
            help=_("Logs file renaming changes if grouping by renaming, or it logs the file "
                   "copying/movement if grouping by folders. If no log file is specified  with "
                   "'--log-file', then a 'sort_log.json' file will be created in the input "
                   "directory.")))
        argument_list.append(dict(
            opts=('-lf', '--log-file'),
            action=SaveFileFullPaths,
            filetypes="alignments",
            group=_("settings"),
            dest='log_file_path',
            default='sort_log.json',
            help=_("Specify a log file to use for saving the renaming or grouping information. If "
                   "specified extension isn't 'json' or 'yaml', then json will be used as the "
                   "serializer, with the supplied filename. Default: sort_log.json")))

        return argument_list
