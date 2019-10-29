/**
 * @fileoverview gRPC-Web generated client stub for burstout
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!



const grpc = {};
grpc.web = require('grpc-web');

const proto = {};
proto.burstout = require('./main_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.burstout.MainInterfaceClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

  /**
   * @private @const {?Object} The credentials to be used to connect
   *    to the server
   */
  this.credentials_ = credentials;

  /**
   * @private @const {?Object} Options for the client
   */
  this.options_ = options;
};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.burstout.MainInterfacePromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

  /**
   * @private @const {?Object} The credentials to be used to connect
   *    to the server
   */
  this.credentials_ = credentials;

  /**
   * @private @const {?Object} Options for the client
   */
  this.options_ = options;
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Space>}
 */
const methodDescriptor_MainInterface_user_space_scan = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/user_space_scan',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.burstout.UUID,
  proto.burstout.Space,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Space.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Space>}
 */
const methodInfo_MainInterface_user_space_scan = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.Space,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Space.deserializeBinary
);


/**
 * @param {!proto.burstout.UUID} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.Space>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.user_space_scan =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/user_space_scan',
      request,
      metadata || {},
      methodDescriptor_MainInterface_user_space_scan);
};


/**
 * @param {!proto.burstout.UUID} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.Space>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfacePromiseClient.prototype.user_space_scan =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/user_space_scan',
      request,
      metadata || {},
      methodDescriptor_MainInterface_user_space_scan);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.UUID,
 *   !proto.burstout.JWTToken>}
 */
const methodDescriptor_MainInterface_get_user_twilio_token = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/get_user_twilio_token',
  grpc.web.MethodType.UNARY,
  proto.burstout.UUID,
  proto.burstout.JWTToken,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.JWTToken.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.UUID,
 *   !proto.burstout.JWTToken>}
 */
const methodInfo_MainInterface_get_user_twilio_token = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.JWTToken,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.JWTToken.deserializeBinary
);


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.burstout.JWTToken)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.JWTToken>|undefined}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.get_user_twilio_token =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/burstout.MainInterface/get_user_twilio_token',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_user_twilio_token,
      callback);
};


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.burstout.JWTToken>}
 *     A native promise that resolves to the response
 */
proto.burstout.MainInterfacePromiseClient.prototype.get_user_twilio_token =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/burstout.MainInterface/get_user_twilio_token',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_user_twilio_token);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.UUID,
 *   !proto.burstout.User>}
 */
const methodDescriptor_MainInterface_get_user = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/get_user',
  grpc.web.MethodType.UNARY,
  proto.burstout.UUID,
  proto.burstout.User,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.User.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.UUID,
 *   !proto.burstout.User>}
 */
const methodInfo_MainInterface_get_user = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.User,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.User.deserializeBinary
);


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.burstout.User)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.User>|undefined}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.get_user =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/burstout.MainInterface/get_user',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_user,
      callback);
};


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.burstout.User>}
 *     A native promise that resolves to the response
 */
proto.burstout.MainInterfacePromiseClient.prototype.get_user =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/burstout.MainInterface/get_user',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_user);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Organization>}
 */
const methodDescriptor_MainInterface_get_organization = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/get_organization',
  grpc.web.MethodType.UNARY,
  proto.burstout.UUID,
  proto.burstout.Organization,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Organization.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Organization>}
 */
const methodInfo_MainInterface_get_organization = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.Organization,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Organization.deserializeBinary
);


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.burstout.Organization)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.Organization>|undefined}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.get_organization =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/burstout.MainInterface/get_organization',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_organization,
      callback);
};


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.burstout.Organization>}
 *     A native promise that resolves to the response
 */
proto.burstout.MainInterfacePromiseClient.prototype.get_organization =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/burstout.MainInterface/get_organization',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_organization);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Message>}
 */
const methodDescriptor_MainInterface_get_message = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/get_message',
  grpc.web.MethodType.UNARY,
  proto.burstout.UUID,
  proto.burstout.Message,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Message.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Message>}
 */
const methodInfo_MainInterface_get_message = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.Message,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Message.deserializeBinary
);


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.burstout.Message)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.Message>|undefined}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.get_message =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/burstout.MainInterface/get_message',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_message,
      callback);
};


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.burstout.Message>}
 *     A native promise that resolves to the response
 */
proto.burstout.MainInterfacePromiseClient.prototype.get_message =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/burstout.MainInterface/get_message',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_message);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Space>}
 */
const methodDescriptor_MainInterface_get_space = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/get_space',
  grpc.web.MethodType.UNARY,
  proto.burstout.UUID,
  proto.burstout.Space,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Space.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Space>}
 */
const methodInfo_MainInterface_get_space = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.Space,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Space.deserializeBinary
);


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.burstout.Space)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.Space>|undefined}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.get_space =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/burstout.MainInterface/get_space',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_space,
      callback);
};


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.burstout.Space>}
 *     A native promise that resolves to the response
 */
proto.burstout.MainInterfacePromiseClient.prototype.get_space =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/burstout.MainInterface/get_space',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_space);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Channel>}
 */
const methodDescriptor_MainInterface_get_channel = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/get_channel',
  grpc.web.MethodType.UNARY,
  proto.burstout.UUID,
  proto.burstout.Channel,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Channel.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.UUID,
 *   !proto.burstout.Channel>}
 */
const methodInfo_MainInterface_get_channel = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.Channel,
  /** @param {!proto.burstout.UUID} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Channel.deserializeBinary
);


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.burstout.Channel)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.Channel>|undefined}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.get_channel =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/burstout.MainInterface/get_channel',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_channel,
      callback);
};


/**
 * @param {!proto.burstout.UUID} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.burstout.Channel>}
 *     A native promise that resolves to the response
 */
proto.burstout.MainInterfacePromiseClient.prototype.get_channel =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/burstout.MainInterface/get_channel',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_channel);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.BatchReq,
 *   !proto.burstout.ScanResult>}
 */
const methodDescriptor_MainInterface_get_message_batch = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/get_message_batch',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.burstout.BatchReq,
  proto.burstout.ScanResult,
  /** @param {!proto.burstout.BatchReq} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.ScanResult.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.BatchReq,
 *   !proto.burstout.ScanResult>}
 */
const methodInfo_MainInterface_get_message_batch = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.ScanResult,
  /** @param {!proto.burstout.BatchReq} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.ScanResult.deserializeBinary
);


/**
 * @param {!proto.burstout.BatchReq} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.ScanResult>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.get_message_batch =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/get_message_batch',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_message_batch);
};


/**
 * @param {!proto.burstout.BatchReq} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.ScanResult>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfacePromiseClient.prototype.get_message_batch =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/get_message_batch',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_message_batch);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.Cursor,
 *   !proto.burstout.ScanResult>}
 */
const methodDescriptor_MainInterface_get_user_batch = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/get_user_batch',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.burstout.Cursor,
  proto.burstout.ScanResult,
  /** @param {!proto.burstout.Cursor} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.ScanResult.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.Cursor,
 *   !proto.burstout.ScanResult>}
 */
const methodInfo_MainInterface_get_user_batch = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.ScanResult,
  /** @param {!proto.burstout.Cursor} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.ScanResult.deserializeBinary
);


/**
 * @param {!proto.burstout.Cursor} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.ScanResult>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.get_user_batch =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/get_user_batch',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_user_batch);
};


/**
 * @param {!proto.burstout.Cursor} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.ScanResult>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfacePromiseClient.prototype.get_user_batch =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/get_user_batch',
      request,
      metadata || {},
      methodDescriptor_MainInterface_get_user_batch);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.Cursor,
 *   !proto.burstout.Message>}
 */
const methodDescriptor_MainInterface_channel_message_scan = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/channel_message_scan',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.burstout.Cursor,
  proto.burstout.Message,
  /** @param {!proto.burstout.Cursor} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Message.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.Cursor,
 *   !proto.burstout.Message>}
 */
const methodInfo_MainInterface_channel_message_scan = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.Message,
  /** @param {!proto.burstout.Cursor} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.Message.deserializeBinary
);


/**
 * @param {!proto.burstout.Cursor} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.Message>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.channel_message_scan =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/channel_message_scan',
      request,
      metadata || {},
      methodDescriptor_MainInterface_channel_message_scan);
};


/**
 * @param {!proto.burstout.Cursor} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.Message>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfacePromiseClient.prototype.channel_message_scan =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/channel_message_scan',
      request,
      metadata || {},
      methodDescriptor_MainInterface_channel_message_scan);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.Cursor,
 *   !proto.burstout.ScanResult>}
 */
const methodDescriptor_MainInterface_scan_messages_in_channel = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/scan_messages_in_channel',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.burstout.Cursor,
  proto.burstout.ScanResult,
  /** @param {!proto.burstout.Cursor} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.ScanResult.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.Cursor,
 *   !proto.burstout.ScanResult>}
 */
const methodInfo_MainInterface_scan_messages_in_channel = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.ScanResult,
  /** @param {!proto.burstout.Cursor} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.ScanResult.deserializeBinary
);


/**
 * @param {!proto.burstout.Cursor} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.ScanResult>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.scan_messages_in_channel =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/scan_messages_in_channel',
      request,
      metadata || {},
      methodDescriptor_MainInterface_scan_messages_in_channel);
};


/**
 * @param {!proto.burstout.Cursor} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.ScanResult>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfacePromiseClient.prototype.scan_messages_in_channel =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/scan_messages_in_channel',
      request,
      metadata || {},
      methodDescriptor_MainInterface_scan_messages_in_channel);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.Cursor,
 *   !proto.burstout.ScanResult>}
 */
const methodDescriptor_MainInterface_scan_channels_in_space = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/scan_channels_in_space',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.burstout.Cursor,
  proto.burstout.ScanResult,
  /** @param {!proto.burstout.Cursor} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.ScanResult.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.Cursor,
 *   !proto.burstout.ScanResult>}
 */
const methodInfo_MainInterface_scan_channels_in_space = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.ScanResult,
  /** @param {!proto.burstout.Cursor} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.ScanResult.deserializeBinary
);


/**
 * @param {!proto.burstout.Cursor} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.ScanResult>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.scan_channels_in_space =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/scan_channels_in_space',
      request,
      metadata || {},
      methodDescriptor_MainInterface_scan_channels_in_space);
};


/**
 * @param {!proto.burstout.Cursor} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.ScanResult>}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfacePromiseClient.prototype.scan_channels_in_space =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/burstout.MainInterface/scan_channels_in_space',
      request,
      metadata || {},
      methodDescriptor_MainInterface_scan_channels_in_space);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.Credentials,
 *   !proto.burstout.AuthResult>}
 */
const methodDescriptor_MainInterface_auth_login = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/auth_login',
  grpc.web.MethodType.UNARY,
  proto.burstout.Credentials,
  proto.burstout.AuthResult,
  /** @param {!proto.burstout.Credentials} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.AuthResult.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.Credentials,
 *   !proto.burstout.AuthResult>}
 */
const methodInfo_MainInterface_auth_login = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.AuthResult,
  /** @param {!proto.burstout.Credentials} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.AuthResult.deserializeBinary
);


/**
 * @param {!proto.burstout.Credentials} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.burstout.AuthResult)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.AuthResult>|undefined}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.auth_login =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/burstout.MainInterface/auth_login',
      request,
      metadata || {},
      methodDescriptor_MainInterface_auth_login,
      callback);
};


/**
 * @param {!proto.burstout.Credentials} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.burstout.AuthResult>}
 *     A native promise that resolves to the response
 */
proto.burstout.MainInterfacePromiseClient.prototype.auth_login =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/burstout.MainInterface/auth_login',
      request,
      metadata || {},
      methodDescriptor_MainInterface_auth_login);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.burstout.Credentials,
 *   !proto.burstout.AuthResult>}
 */
const methodDescriptor_MainInterface_auth_signup = new grpc.web.MethodDescriptor(
  '/burstout.MainInterface/auth_signup',
  grpc.web.MethodType.UNARY,
  proto.burstout.Credentials,
  proto.burstout.AuthResult,
  /** @param {!proto.burstout.Credentials} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.AuthResult.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.burstout.Credentials,
 *   !proto.burstout.AuthResult>}
 */
const methodInfo_MainInterface_auth_signup = new grpc.web.AbstractClientBase.MethodInfo(
  proto.burstout.AuthResult,
  /** @param {!proto.burstout.Credentials} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.burstout.AuthResult.deserializeBinary
);


/**
 * @param {!proto.burstout.Credentials} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.burstout.AuthResult)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.burstout.AuthResult>|undefined}
 *     The XHR Node Readable Stream
 */
proto.burstout.MainInterfaceClient.prototype.auth_signup =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/burstout.MainInterface/auth_signup',
      request,
      metadata || {},
      methodDescriptor_MainInterface_auth_signup,
      callback);
};


/**
 * @param {!proto.burstout.Credentials} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.burstout.AuthResult>}
 *     A native promise that resolves to the response
 */
proto.burstout.MainInterfacePromiseClient.prototype.auth_signup =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/burstout.MainInterface/auth_signup',
      request,
      metadata || {},
      methodDescriptor_MainInterface_auth_signup);
};


module.exports = proto.burstout;

