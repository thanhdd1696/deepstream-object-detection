
import sys
from uuid import uuid4
sys.path.append('../')
import configparser

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst
from deepstream.common.is_aarch_64 import is_aarch64
from deepstream.common.bus_call import bus_call
# from deepstream.common.nvosd import osd_sink_pad_buffer_probe
from deepstream.app.counter import osd_sink_pad_buffer_probe


class Pipeline:
    def __init__(self):
        Gst.init(None)
        self.pipeline = Gst.Pipeline()
        self.source = Gst.ElementFactory.make("filesrc", "file-source")
        self.h264parser = Gst.ElementFactory.make("h264parse", "h264-parser")
        self.decoder = Gst.ElementFactory.make("nvv4l2decoder", "nvv4l2-decoder")
        self.streammux = Gst.ElementFactory.make("nvstreammux", "Stream-muxer")
        self.pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
        self.tracker = Gst.ElementFactory.make("nvtracker", "tracker")
        self.nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")
        self.nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
        self.nvvidconv_postosd = Gst.ElementFactory.make("nvvideoconvert", "convertor_postosd")
        self.caps = Gst.ElementFactory.make("capsfilter", "filter")
        self.encoder = Gst.ElementFactory.make("nvv4l2h264enc", "encoder")
        self.sink = Gst.ElementFactory.make("filesink", "file-sink")
        # if is_aarch64():
        #     self.sink = Gst.ElementFactory.make("nv3dsink", "nv3d-sink")
        # else:
        #     self.sink = Gst.ElementFactory.make("nveglglessink", "nvvideo-renderer")

        config = configparser.ConfigParser()
        config.read('deepstream/source/source_file_config.txt')
        config.sections()

        for key in config['source']:
            if key == 'uri':
                uri = config.get('source', key)
                self.source.set_property('location', uri)

        self.streammux.set_property('width', 1920)
        self.streammux.set_property('height', 1080)
        self.streammux.set_property('batch-size', 1)
        self.streammux.set_property('batched-push-timeout', 4000000)
        self.pgie.set_property('config-file-path', "deepstream/pgie/config_infer_primary_yoloV8.yml")

        config = configparser.ConfigParser()
        config.read('deepstream/tracker/dstest2_tracker_config.txt')
        config.sections()

        for key in config['tracker']:
            if key == 'tracker-width':
                tracker_width = config.getint('tracker', key)
                self.tracker.set_property('tracker-width', tracker_width)
            if key == 'tracker-height':
                tracker_height = config.getint('tracker', key)
                self.tracker.set_property('tracker-height', tracker_height)
            if key == 'gpu-id':
                tracker_gpu_id = config.getint('tracker', key)
                self.tracker.set_property('gpu_id', tracker_gpu_id)
            if key == 'll-lib-file':
                tracker_ll_lib_file = config.get('tracker', key)
                self.tracker.set_property('ll-lib-file', tracker_ll_lib_file)
            if key == 'll-config-file':
                tracker_ll_config_file = config.get('tracker', key)
                self.tracker.set_property('ll-config-file', tracker_ll_config_file)
            if key == 'enable-batch-process':
                tracker_enable_batch_process = config.getint('tracker', key)
                self.tracker.set_property('enable_batch_process', tracker_enable_batch_process)
            if key == 'enable-past-frame':
                tracker_enable_past_frame = config.getint('tracker', key)
                self.tracker.set_property('enable_past_frame', tracker_enable_past_frame)

        self.caps.set_property("caps", Gst.Caps.from_string("video/x-raw(memory:NVMM), format=I420"))
        self.encoder.set_property('bitrate', 4000000)

        self.pipeline.add(self.source)
        self.pipeline.add(self.h264parser)
        self.pipeline.add(self.decoder)
        self.pipeline.add(self.streammux)
        self.pipeline.add(self.pgie)
        self.pipeline.add(self.tracker)
        self.pipeline.add(self.nvvidconv)
        self.pipeline.add(self.nvosd)
        self.pipeline.add(self.nvvidconv_postosd)
        self.pipeline.add(self.caps)
        self.pipeline.add(self.encoder)
        self.pipeline.add(self.sink)

        print("Linking elements in the Pipeline \n")

        self.source.link(self.h264parser)
        self.h264parser.link(self.decoder)
        sinkpad = self.streammux.get_request_pad("sink_0")
        if not sinkpad:
            sys.stderr.write(" Unable to get the sink pad of streammux \n")
        srcpad = self.decoder.get_static_pad("src")
        if not srcpad:
            sys.stderr.write(" Unable to get source pad of decoder \n")
        srcpad.link(sinkpad)
        self.streammux.link(self.pgie)
        self.pgie.link(self.tracker)
        self.tracker.link(self.nvvidconv)
        self.nvvidconv.link(self.nvosd)
        self.nvosd.link(self.nvvidconv_postosd)
        self.nvvidconv_postosd.link(self.caps)
        self.caps.link(self.encoder)
        self.encoder.link(self.sink)

        self.loop = GLib.MainLoop()

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", bus_call, self.loop)

        # Lets add probe to get informed of the meta data generated, we add probe to
        # the sink pad of the osd element, since by that time, the buffer would have
        # had got all the metadata.
        osdsinkpad = self.nvosd.get_static_pad("sink")
        if not osdsinkpad:
            sys.stderr.write(" Unable to get sink pad of nvosd \n")
        osdsinkpad.add_probe(Gst.PadProbeType.BUFFER, osd_sink_pad_buffer_probe, 0)

    def start(self, inference_id):
        output_file = f"shared_folder/annotated_videos/output-{inference_id}.mp4"
        self.sink.set_property('location', output_file)
        self.pipeline.set_state(Gst.State.PLAYING)
        try:
            self.loop.run()
        except:
            pass

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.loop.quit()


pipeline = Pipeline()
