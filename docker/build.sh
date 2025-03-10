#!/bin/bash

export DOCKER_BUILDKIT=1
export UBUNTU_VERSION="20.04"
export PYTHON_VERSION="3.9-slim-bullseye"
build_base_image () {
        docker pull ubuntu:"$UBUNTU_VERSION"
	docker build ../ -f Dockerfile-base -t arcor2/arcor2_base:"$VERSION" --build-arg version="$UBUNTU_VERSION"
}

build_dist_base_image () {
    #    docker pull python:"$PYTHON_VERSION"
	#docker build -f Dockerfile-dist-base -t arcor2/arcor2_dist_base:"$VERSION"  ../ --build-arg version="$PYTHON_VERSION"
	VERSION="latest" ./pants package docker:dist-base
}

build_arserver_image () {
	#docker build -f Dockerfile-arserver -t arcor2/arcor2_arserver:"$(cat ../src/python/arcor2_arserver/VERSION)"  ../ --build-arg version="$VERSION"
	VERSION=$(cat src/python/arcor2_arserver/VERSION) ./pants package docker:arserver
}

build_build_image () {
	#docker build -f Dockerfile-build -t arcor2/arcor2_build:"$(cat ../src/python/arcor2_build/VERSION)" --build-arg version="$VERSION" ../
	VERSION=$(cat src/python/arcor2_build/VERSION) ./pants package docker:build
}

build_execution_image () {
	#docker build -f Dockerfile-execution -t arcor2/arcor2_execution:"$(cat ../src/python/arcor2_execution/VERSION)" --build-arg version="$VERSION" ../
	VERSION=$(cat src/python/arcor2_execution/VERSION) ./pants package docker:execution
}

build_kinect_azure () {
	docker build -f Dockerfile-kinect-azure -t arcor2/arcor2_kinect_azure:"$(cat ../src/python/arcor2_kinect_azure/VERSION)" --build-arg version="$VERSION" ../
}

build_execution_proxy_image () {
	docker build -f Dockerfile-execution-proxy -t arcor2/arcor2_execution_proxy:"$(cat ../src/python/arcor2_execution_rest_proxy/VERSION)" --build-arg version="$VERSION" ../
}

build_mocks_image () {
	#docker build -f Dockerfile-mocks -t arcor2/arcor2_mocks:"$(cat ../src/python/arcor2_mocks/VERSION)" --build-arg version="$VERSION" ../
	VERSION=$(cat src/python/arcor2_mocks/VERSION) ./pants package docker:mocks
}

build_devel_image () {
	docker build -f Dockerfile-devel -t arcor2/arcor2_devel:"$VERSION" --build-arg version="$VERSION" ../
}

build_upload_fit_demo_image () {
	#docker build -f Dockerfile-upload-fit-demo -t arcor2/arcor2_upload_fit_demo:"$(cat ../src/python/arcor2_fit_demo/VERSION)" --build-arg version="$VERSION" ../
	VERSION=$(cat src/python/arcor2_fit_demo/VERSION) ./pants package docker:upload_fit_demo
}

build_upload_builtin_objects_image () {
	docker build -f Dockerfile-upload-builtin-objects -t arcor2/arcor2_upload_builtin_objects:"$(cat ../src/python/arcor2/VERSION)" --build-arg version="$VERSION" ../
}

build_dobot_image () {
	#docker build -f Dockerfile-dobot -t arcor2/arcor2_dobot:"$(cat ../src/python/arcor2_dobot/VERSION)" --build-arg version="$VERSION" ../
	VERSION=$(cat src/python/arcor2_dobot/VERSION) ./pants package docker:dobot
}

build_calibration_image () {
	#docker build -f Dockerfile-calibration -t arcor2/arcor2_calibration:"$(cat ../src/python/arcor2_calibration/VERSION)" --build-arg version="$VERSION" ../
	VERSION=$(cat src/python/arcor2_calibration/VERSION) ./pants package docker:calibration
}

build_fanuc_image () {
	docker build -f Dockerfile-fanuc -t arcor2/arcor2_fanuc:"$(cat ../src/python/arcor2_fanuc/VERSION)" --build-arg version="$VERSION" ../
}

build_fanuc_objects_image () {
	docker build -f Dockerfile-upload-fanuc-objects -t arcor2/arcor2_fanuc_upload_object_types:"$(cat ../src/python/arcor2_fanuc/VERSION)" --build-arg version="$VERSION" ../
}

build_all_images() {
	build_dist_base_image
	build_arserver_image
	build_build_image
	build_execution_image
	build_execution_proxy_image
	build_kinect_azure
	build_mocks_image
	build_devel_image
	build_upload_fit_demo_image
	build_upload_builtin_objects_image
	build_dobot_image
	build_calibration_image
	build_fanuc_image
	build_fanuc_objects_image
}

if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "sudo sh build.sh VERSION [arserver] [build] [execution] [execution-proxy] [kinect-azure] [mocks] [devel] [dobot] [calibration] [upload-fit-demo] [upload-builtin] [fanuc] [fanuc-objects]"
    echo "sudo sh build.sh VERSION all"
    echo "$VERSION specifies version of base image. Optional parameters specifies which images should be build using version from their VERSION file."
    echo "If no optional parameter is specified, base image is build with version $VERSION."
    echo "If second parameter is 'all', all other parameters are ignored and all images are build."
    exit 1
fi

VERSION="$1"

#if [ $# -eq 1 ]; then
#	build_base_image
#	exit 0
#fi

build_dist_base_image

if [ "$2" = 'all' ]; then
    build_all_images
    exit 0
fi


for var in "$@"
do
    if [ "$var" = "$1" ]; then
        continue
    fi
    if [ "$var" = "arserver" ]; then
    	build_arserver_image
	elif [ "$var" = "build" ]; then
    	build_build_image
	elif [ "$var" = "execution" ]; then
    	build_execution_image
	elif [ "$var" = "execution-proxy" ]; then
    	build_execution_proxy_image
	elif [ "$var" = "kinect-azure" ]; then
        build_kinect_azure
    elif [ "$var" = "mocks" ]; then
    	build_mocks_image
	elif [ "$var" = "devel" ]; then
    	build_devel_image
	elif [ "$var" = "dobot" ]; then
    	build_dobot_image
	elif [ "$var" = "calibration" ]; then
    	build_calibration_image
	elif [ "$var" = "upload-fit-demo" ]; then
    	build_upload_fit_demo_image
	elif [ "$var" = "upload-builtin" ]; then
    	build_upload_builtin_objects_image
  elif [ "$var" = "fanuc" ]; then
    	build_fanuc_image
  elif [ "$var" = "fanuc-objects" ]; then
    	build_fanuc_objects_image
	else
	    echo "Unknown image $var"
            exit 0
	fi
done