package(
    default_visibility = ["//visibility:public"],
    licenses = ["notice"],
)

# Tests
# =====
py_test(
    name = "node_test",
    srcs = ["node_test.py"],
    srcs_version = "PY3",
    deps = [
        # already_there/absl/testing:absltest
        "//temporian",
        "//temporian/core/test:utils",
        "//temporian/implementation/numpy/data:event_set",
    ],
)
