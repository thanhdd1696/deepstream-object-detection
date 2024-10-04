from gi.repository import GLib, Gst
import pyds

from random import randint
from routers.start import publisher

PGIE_CLASS_ZERO = 0
PGIE_CLASS_ONE = 1
past_tracking_meta = [0]
TRACKER_MAX_COUNT = [0]

def osd_sink_pad_buffer_probe(pad,info,u_data):

    frame_number = 0
    #Intiallizing object counter with 0.
    obj_counter = {
        PGIE_CLASS_ONE: 0,
        PGIE_CLASS_ZERO: 0
    }
    num_rects=0
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        print("Unable to get GstBuffer ")
        return

    # Retrieve batch metadata from the gst_buffer
    # Note that pyds.gst_buffer_get_nvds_batch_meta() expects the
    # C address of gst_buffer as input, which is obtained with hash(gst_buffer)
    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    l_frame = batch_meta.frame_meta_list
    while l_frame is not None:
        try:
            # Note that l_frame.data needs a cast to pyds.NvDsFrameMeta
            # The casting is done by pyds.NvDsFrameMeta.cast()
            # The casting also keeps ownership of the underlying memory
            # in the C code, so the Python garbage collector will leave
            # it alone.
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break
        l_obj = frame_meta.obj_meta_list
        while l_obj is not None:
            try:
                # Casting l_obj.data to pyds.NvDsObjectMeta
                obj_meta=pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break
            if obj_meta.object_id > TRACKER_MAX_COUNT[0]:
                TRACKER_MAX_COUNT[0] = obj_meta.object_id
                publisher.publish_message(TRACKER_MAX_COUNT[0])
            try:
                l_obj=l_obj.next
            except StopIteration:
                break
        try:
            l_frame=l_frame.next
        except StopIteration:
            break

    return Gst.PadProbeReturn.OK
