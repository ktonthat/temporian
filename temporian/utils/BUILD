load("@bazel_skylib//:bzl_library.bzl", "bzl_library")

package(
    default_visibility = ["//visibility:public"],
    licenses = ["notice"],
)

# Bzl Libraries
# =============

bzl_library(
    name = "compile_bzl",
    srcs = ["compile.bzl"],
)

# Libraries
# =========

py_library(
    name = "string",
    srcs = ["string.py"],
    srcs_version = "PY3",
)

py_library(
    name = "config",
    srcs = ["config.py"],
    srcs_version = "PY3",
)

py_library(
    name = "rtcheck",
    srcs = ["rtcheck.py"],
    srcs_version = "PY3",
)
