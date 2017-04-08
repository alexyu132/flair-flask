var gn = new GyroNorm();
var oldTime, elapsed = 0;
var xPos = 0,
    yPos = 0,
    zPos = 0,
    xVel = 0,
    yVel = 0,
    zVel = 0;

var args = {
    frequency: 20, // ( How often the object sends the values - milliseconds )
    gravityNormalized: true, // ( If the garvity related values to be normalized )
    orientationBase: GyroNorm.GAME, // ( Can be GyroNorm.GAME or GyroNorm.WORLD. gn.GAME returns orientation values with respect to the head direction of the device. gn.WORLD returns the orientation values with respect to the actual north direction of the world. )
    decimalCount: 2, // ( How many digits after the decimal point will there be in the return values )
    logger: null, // ( Function to be called to log messages from gyronorm.js )
    screenAdjusted: false // ( If set to true it will return screen adjusted values. )
};

const SMALL_VALUE_CUTOFF = 0.05;

function filter(value) {
    if (Math.abs(value) < SMALL_VALUE_CUTOFF) return 0;

    return value;
}


gn.init(args).then(function() {


    gn.start(function(data) {

        if (oldTime) {
            elapsed = performance.now() - oldTime;
            xVel += elapsed / 1000 * filter(data.dm.x);
            yVel += elapsed / 1000 * filter(data.dm.y);
            zVel += elapsed / 1000 * filter(data.dm.z);
            xPos += elapsed / 1000 * filter(xVel);
            yPos += elapsed / 1000 * filter(yVel);
            zPos += elapsed / 1000 * filter(zVel);

            console.log(elapsed);
        }

        oldTime = performance.now();

        document.getElementById("xAccelFT").innerHTML = data.dm.x;
        document.getElementById("yAccelFT").innerHTML = data.dm.y;
        document.getElementById("zAccelFT").innerHTML = data.dm.z;

        document.getElementById("alpha").innerHTML = xVel;
        document.getElementById("beta").innerHTML = yVel;
        document.getElementById("gamma").innerHTML = zVel;

        document.getElementById("xPos").innerHTML = xPos;
        document.getElementById("yPos").innerHTML = yPos;
        document.getElementById("zPos").innerHTML = zPos;
        // Process:
        // data.do.alpha	( deviceorientation event alpha value )
        // data.do.beta		( deviceorientation event beta value )
        // data.do.gamma	( deviceorientation event gamma value )
        // data.do.absolute	( deviceorientation event absolute value )

        // data.dm.x		( devicemotion event acceleration x value )
        // data.dm.y		( devicemotion event acceleration y value )
        // data.dm.z		( devicemotion event acceleration z value )

        // data.dm.gx		( devicemotion event accelerationIncludingGravity x value )
        // data.dm.gy		( devicemotion event accelerationIncludingGravity y value )
        // data.dm.gz		( devicemotion event accelerationIncludingGravity z value )

        // data.dm.alpha	( devicemotion event rotationRate alpha value )
        // data.dm.beta		( devicemotion event rotationRate beta value )
        // data.dm.gamma	( devicemotion event rotationRate gamma value )
    });
}).catch(function(e) {
    // Catch if the DeviceOrientation or DeviceMotion is not supported by the browser or device
});
