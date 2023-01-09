This project consists of a ray-tracing renderer following the implementation outlined in chapters 2–4 of [Gabriel Gambetta's](https://gabrielgambetta.com) *Computer Graphics From Scratch*, available for purchase [here](https://nostarch.com/computer-graphics-scratch).

A demo script exists for each applicable chapter of the book. For example, run `chapter_2.py` to output the scene depicted at the end of Chapter 2.

This repository consists of the following project components:

1. A **renderer package** that handles the meat of the ray-tracing tasks. This package is contained with the `/renderer` subdirectory.

2. A **modeler package** that provides classes and tools to describe the 3D scene to be rendered. This package is contained within the `/modeler` subdirectory.

## Development Map
The development of this minute system of packages will, in general, follow the progression of chapters in *Computer Graphics From Scratch*. This timeline is fundamentally constructed around the development of the `renderer` package.

* [&#10003;] **Chapter 2: Basic Raytracing**

* [&#10003;] **Chapter 3: Lighting**

* [&#10003;] **Chapter 4: Shadows and Reflections**

* [--] **Extended Features and Optimizations**
    * [&#10003;] Support for arbitrary camera position and rotation
    * [&#10003;] Triangle primitive
    * [&#10003;] Geometry primitive (Mesh) supporting complex arrangements of Triangles
    * [--] Refactor
    * [--] Render optimizations
    