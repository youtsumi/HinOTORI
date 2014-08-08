module HinOTORI {
	exception Error {
		string reason;
	};

	interface Camera { 
		["amd"] void Take( double expt, string filename, bool shutter )
			throws Error;
		double GetTemperature(  );
		void SetTemperature(  );
	};

	interface Telescope{ 
	};

};
